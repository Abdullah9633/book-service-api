from fastapi import APIRouter, Depends, status, BackgroundTasks
from src.db.main import get_the_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from .schemas import (
    UserCreateModel,
    UserModel,
    UserLoginModel,
    UserBooksReviewsModel,
    EmailModel,
    PasswordResetRequestModel,
    PasswordResetConfirmModel,
)
from .service import UserService
from .utils import (
    create_access_token,
    decode_token,
    verify_password,
    create_the_url_safe_token,
    decode_the_url_safe_token,
    generate_password_hash,
)
from .dependencies import (
    MyRefreshTokenBearer,
    MyAccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from src.db.redis import add_to_blocklist
from src.errors import UserAlreadyExists, InvalidCredentials, InvalidToken, UserNotFound
from src.mail import (
    the_mail,
    create_the_message,
    create_verification_message,
    create_password_reset_message,
)
from src.config import my_config
from src.celery_tasks import send_the_email, my_celery_app


refresh_token_bearer = MyRefreshTokenBearer()
user_service = UserService()
auth_router = APIRouter()
role_checker = RoleChecker(["admin", "user"])
admin_role_checker = RoleChecker(["admin"])


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user_account(
    user_data: UserCreateModel,
    my_bg_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_the_session),
):
    email = user_data.email

    user_exists = await user_service.user_exists(email, session)

    if user_exists:
        raise UserAlreadyExists()

    new_user = await user_service.create_user(user_data, session)

    the_token = create_the_url_safe_token({"an_email": email})

    the_link = f"http://{my_config.DOMAIN}/api/1.0.0/auth/verify/{the_token}"
    the_subject = "Verify your email"

    the_task_id = send_the_email.delay(email, the_subject, new_user.first_name, the_link)

    return {
        "message": "Account Created! Please check your email to verify your account",
        "user": new_user,
        "Task ID": the_task_id.id
    }


from celery.result import AsyncResult
@auth_router.get("/check-task_completion/{task_id}")
async def check_task_completion(task_id):
    task_result = AsyncResult(task_id, app= my_celery_app)
    
    if task_result.state == 'PENDING':
        return {"status": "Task does not finished yet."}
        
    elif task_result.state == 'SUCCESS':
        return {
            "status": "Finished!", 
            "result": task_result.result
        }


@auth_router.get("/verify/{his_token}")
async def verify_user_account(
    his_token: str, session: AsyncSession = Depends(get_the_session)
):

    token_data = decode_the_url_safe_token(his_token)
    user_email = token_data.get("an_email")

    if user_email is not None:
        user = await user_service.get_user_by_email(user_email, session)

        if user is None:
            raise UserNotFound()

        await user_service.update_user(user, {"is_verified": True}, session)

        return JSONResponse(
            content={"message": "User verified successfully"},
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "An error occured during verification"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@auth_router.post("/login")
async def login_users(
    login_data: UserLoginModel, session: AsyncSession = Depends(get_the_session)
):
    email = login_data.email
    password = login_data.password_hash

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid = verify_password(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                    "role": user.role,
                }
            )

            refresh_token = create_access_token(
                user_data={
                    "email": user.email,
                    "user_uid": str(user.uid),
                    "role": user.role,
                },
                refresh=True,
                expiry=timedelta(days=3),
            )

            return JSONResponse(
                content={
                    "message": "Login Successful!",
                    "access token": access_token,
                    "refresh token": refresh_token,
                    "user": {"email": user.email, "user_uid": str(user.uid)},
                }
            )

    raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details=Depends(refresh_token_bearer)):

    the_expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(the_expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details["user"])

        return JSONResponse(
            content={
                "message": "New access Token Created!",
                "access token": new_access_token,
                "user": {
                    "email": token_details["user"]["email"],
                    "user_uid": token_details["user"]["user_uid"],
                },
            }
        )

    raise InvalidToken()


@auth_router.get("/logout")
async def revoke_token(token_details=Depends(MyAccessTokenBearer())):
    jti = token_details["jti"]

    await add_to_blocklist(jti)

    return JSONResponse(
        content={"message": "Logged out successfully!"}, status_code=status.HTTP_200_OK
    )


@auth_router.get("/me", response_model=UserBooksReviewsModel)
async def get_the_current_user(user=Depends(get_current_user)):
    return user


@auth_router.post("/send_email")
async def send_the_mail(emails: EmailModel):
    the_addresses = emails.email_addresses

    the_subject = "The Welcome point"
    the_html_message = (
        "<h1>Welcome to our Application!</h1> <p>We hope that you will enjoy alot</p>"
    )

    my_message = create_the_message(
        the_recipients=the_addresses,
        the_subject=the_subject,
        the_body=the_html_message,
    )

    # await the_mail.send_message(message= my_message)
    await the_mail.send_message(message=my_message, template_name="welcome_email.html")

    return {"message": "Email sent Successfully"}


@auth_router.post("/password-reset-request")
async def password_reset_request(email_data: PasswordResetRequestModel):
    email = email_data.email

    the_token = create_the_url_safe_token({"an_email": email})

    the_link = f"http://{my_config.DOMAIN}/api/1.0.0/auth/password_reset_confirm_frontend/{the_token}"

    my_message = create_password_reset_message(
        the_recipients=[email], the_subject="Reset your Password", the_link=the_link
    )

    await the_mail.send_message(
        message=my_message, template_name="password_reset_email.html"
    )

    return JSONResponse(
        content={
            "Message": "Please check your Email for instructions to reset your password",
            "link": the_link,
        },
        status_code=status.HTTP_200_OK,
    )


from fastapi.responses import FileResponse


@auth_router.get("/password_reset_confirm_frontend/{token}")
async def reset_password_frontend(token, session=Depends(get_the_session)):

    token_data = decode_the_url_safe_token(token)
    user_email = token_data.get("an_email")

    if user_email is not None:
        user = await user_service.get_user_by_email(user_email, session)

        if user is None:
            raise UserNotFound()

        from pathlib import Path

        # Gets the directory of 'codefile', goes up one level to 'src'
        BASE_DIR = Path(__file__).resolve().parent.parent
        index_path = BASE_DIR / "static" / "index.html"

        return FileResponse(index_path)

    return JSONResponse(
        content={"message": "An error occured during password reset"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


from fastapi import Form


@auth_router.post("/password-reset-submit")
async def reset_password(
    confirm_new_password: str = Form(),
    token: str = Form(),
    new_password: str = Form(),
    description: str = Form(None),
    session: AsyncSession = Depends(get_the_session),
):

    if new_password != confirm_new_password:
        raise HTTPException(
            detail="Passwords don't match", status_code=status.HTTP_400_BAD_REQUEST
        )

    token_data = decode_the_url_safe_token(token)
    user_email = token_data.get("an_email")

    if user_email is not None:
        user = await user_service.get_user_by_email(user_email, session)

        if user is None:
            raise UserNotFound()

        password_hash = generate_password_hash(password=new_password)
        await user_service.update_user(user, {"password_hash": password_hash}, session)

        return JSONResponse(
            content={
                "message": "Password reset successfully",
                "description": description,
            },
            status_code=status.HTTP_200_OK,
        )

    return JSONResponse(
        content={"message": "An error occured during password reset"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
