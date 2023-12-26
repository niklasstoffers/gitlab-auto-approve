from pydantic import BaseModel, model_validator, FilePath, ValidationError

class SSL(BaseModel):
    enable: bool
    key_file: FilePath | None = None
    cert_file: FilePath | None = None

    @model_validator(mode='after')
    def _validate_certs(self) -> 'SSL':
        if self.enable and (self.key_file is None or self.cert_file is None):
            raise ValidationError("Certificate and key file are required with SSL enabled")
        return self