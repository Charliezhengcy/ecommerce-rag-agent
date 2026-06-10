class StaticFileService:
    """Keeps static URL behavior explicit for future CDN replacement."""

    @staticmethod
    def dataset_url(image_path: str) -> str:
        return f"/static/dataset/{image_path.lstrip('/')}"

