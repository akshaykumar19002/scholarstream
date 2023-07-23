def check_if_user_has_subscription(user):
    return user.subscription_set.filter(
        is_active=True,
    ).exists()