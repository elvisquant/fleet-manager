from fastapi import FastAPI
# Assuming your user router file is at 'app/routes/user.py'
# and your new category router file is at 'app/routes/user_category.py'
from app.routes import user, user_category 

def create_application():
    application = FastAPI(
        title="My Professional Portal API",
        description="API for managing users and their roles.",
        version="1.0.0"
    )
    
    # --- Registering Routers ---
    
    # User and Auth Routers
    application.include_router(user.user_router)
    application.include_router(user.guest_router)
    application.include_router(user.auth_router)
    
    # 1. Register the new router for managing user categories
    application.include_router(user_category.category_router)
    
    return application


app = create_application()


@app.get("/")
async def root():
    return {"message": "Hi, I am Describly. Awesome - Your setup is done & working."}