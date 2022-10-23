from django.core.exceptions import ValidationError


def size_validator(file):
    if file.size > 5 * 1024 * 1024:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    else:
        return file
