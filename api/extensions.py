import os
from vercel.blob import BlobClient, ListBlobItem
from flask import g
from celery import Celery, Task
from flask import Flask

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

def get_blob_client() -> BlobClient:
    if "blob_client" not in g:
        g.blob_client = BlobClient(
            token=os.environ.get("BLOB_READ_WRITE_TOKEN", "")
        )

    return g.blob_client

def list_images() -> list[ListBlobItem]:
    blob_client = get_blob_client()
    blobs = blob_client.list_objects(mode="folded")
    first_folder = blobs.folders[0]
    sub = blob_client.list_objects(prefix=first_folder, mode="folded")
    return sub.blobs