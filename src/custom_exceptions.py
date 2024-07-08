class AccessDenied(Exception):
    pass


class BucketAlreadyExists(Exception):
    pass


class BucketAlreadyOwnedByYou(Exception):
    pass


class BucketNotEmpty(Exception):
    pass


class InvalidBucketName(Exception):
    pass


class InvalidParameterException(Exception):
    pass


class InvalidRequest(Exception):
    pass


class MalformedXML(Exception):
    pass


class NoSuchBucket(Exception):
    pass


class NoSuchKey(Exception):
    pass


class NoSuchTable(Exception):
    pass


class ParameterNotFound(Exception):
    pass


class ResourceExistsException(Exception):
    pass


class ResourceNotFoundException(Exception):
    pass


class ValidationException(Exception):
    pass


error_map = {
    "AccessDenied": AccessDenied,
    "BucketAlreadyExists": BucketAlreadyExists,
    "BucketAlreadyOwnedByYou": BucketAlreadyOwnedByYou,
    "BucketNotEmpty": BucketNotEmpty,
    "InvalidBucketName": InvalidBucketName,
    "InvalidParameterException": InvalidParameterException,
    "InvalidRequest": InvalidRequest,
    "MalformedXML": MalformedXML,
    "NoSuchBucket": NoSuchBucket,
    "NoSuchKey": NoSuchKey,
    "ParameterNotFound": ParameterNotFound,
    "ResourceExistsException": ResourceExistsException,
    "ResourceNotFoundException": ResourceNotFoundException,
    "ValidationException": ValidationException,
}


def error_handler(e):
    """Raises a custom exception class given a Boto3 error response.

    Checks the values of "Code" and "Message" in the error response dictionary
    and uses these values to select the custom exception and returned message
    respectively. Used to catch and raise exceptions in the error_map above.

    Usage of this function should be followed by a `raise ClientError` at the
    same level of indentation in order to re-raise the error if it hasn't been
    accounted for by one of the custom exceptions.

    Args:
        e: A Boto3 response dictionary, expected to contain a nested
        dictionary under the key "Error". The nested dictionary is expected
        to have "Code" and "Message" keys.

    Returns:
        None

    Raises:
        A custom exception named after the "Code" in the Boto3 error response.
    """
    error_body = e.response["Error"]
    error_code = error_body["Code"]
    error_msg = error_body["Message"]

    if error_code in error_map:
        raise error_map[error_code](error_msg)
