GET_HEALTH_CHECK = {
    "method": "GET",
    "operation_id": "Accounts Health Check",
    "operation_description": "Returns service status for the accounts module.",
    "responses": {
        200: "Service is healthy",
    },
    "tags": ["accounts"],
}

POST_LOGIN = {
    "method": "POST",
    "operation_id": "Login",
    "operation_description": (
        "Authenticate with email and password.\n\n"
        "Returns session cookie on success.\n\n"
        "Permissions:\n- Anyone (no authentication required)"
    ),
    "responses": {
        200: "Login successful",
        400: "Invalid credentials",
    },
    "tags": ["accounts"],
}

POST_LOGOUT = {
    "method": "POST",
    "operation_id": "Logout",
    "operation_description": (
        "Invalidate the current session.\n\n"
        "Permissions:\n- Authenticated users only"
    ),
    "responses": {
        200: "Logged out successfully",
        401: "Not authenticated",
    },
    "tags": ["accounts"],
}

GET_ME = {
    "method": "GET",
    "operation_id": "Get My Profile",
    "operation_description": (
        "Returns the profile of the currently authenticated user.\n\n"
        "Permissions:\n- Authenticated users only"
    ),
    "responses": {
        200: "User profile",
        401: "Not authenticated",
    },
    "tags": ["accounts"],
}

PATCH_ME = {
    "method": "PATCH",
    "operation_id": "Update My Profile",
    "operation_description": (
        "Partially update the authenticated user's profile.\n\n"
        "Permissions:\n- Authenticated users only"
    ),
    "responses": {
        200: "Profile updated successfully",
        400: "Validation error",
        401: "Not authenticated",
    },
    "tags": ["accounts"],
}

POST_CHANGE_PASSWORD = {
    "method": "POST",
    "operation_id": "Change Password",
    "operation_description": (
        "Change the current user's password.\n\n"
        "Requires the current password for verification.\n\n"
        "Permissions:\n- Authenticated users only"
    ),
    "responses": {
        200: "Password changed successfully",
        400: "Validation error — wrong current password or weak new password",
        401: "Not authenticated",
    },
    "tags": ["accounts"],
}
