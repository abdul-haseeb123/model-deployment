**Project Overview**
- **Repository**: `model-deployment` — contains data transforms, a training notebook, a saved `model.pth`, and an app that uses the trained model.

**How To Get Data**
- **Source**: Download the dataset from Kaggle: `https://www.kaggle.com/datasets/die9origephit/nike-adidas-and-converse-imaged`.
- **Local layout requirement**: Ensure a `data/` directory exists at the repo root with two subfolders: `train/` and `test/` (i.e., `data/train` and `data/test`). Place the downloaded dataset content into those folders before running the transform step.

**Prepare the dataset (run transforms)**
- Run the transform script to create the `images/` folder and `annotations.csv` inside both `data/train` and `data/test`. command:

```
python transform_data.py
```

- After running the command, each of `data/train` and `data/test` will include an `images/` folder and an `annotations.csv` file suitable for training.

**Install Python dependencies**
- There are a few ways to install the project's dependencies. Pick one of the methods below:


- Using `poetry` (if you manage dependency groups in `pyproject.toml`):

```
poetry install --with dev
```

- If your project uses a `dev` dependency group or extras, `poetry` is the recommended approach. Alternatively, if your package exposes an extras group, you can use:

```
pip install -e .[dev]
```

**Install PyTorch**
- Install PyTorch according to your system configuration and GPU availability by following the official instructions and selecting the right CUDA / CPU build: `https://pytorch.org/get-started/locally/`.
- The PyTorch installation command depends on OS, Python version and CUDA version — follow the selector on the page and copy the command it gives you.

**Train the model (run notebook)**
- Open `notebook.ipynb` and run it from top to bottom. The notebook runs the training routine and will save the trained weights to `model.pth` in the repo root when complete.
- Example using Jupyter locally:

```
jupyter notebook notebook.ipynb
```

**Environment variables**
- Populate the provided `.env.example` with your secrets (for example: app token and Redis URL). Create environment files for your run mode:
- **Local dev**: copy to ` .env.local` (used when running the app locally):

```
cp .env.example .env.local
# then edit .env.local and fill TOKEN and REDIS_URL values
```

- **Docker**: copy to `.env.docker` for docker-compose runs:

```
cp .env.example .env.docker
# then edit .env.docker and fill TOKEN and REDIS_URL values
```

**Run the app with Docker**
- The repository includes a `docker-compose.yml`. To start the app and associated services with Docker Compose:

```
docker-compose up --build
# or, on systems with the newer Docker CLI plugin:
docker compose up --build
```

- The compose stack will use the `.env.docker` file if you name and configure it accordingly, or you can export environment variables before running.

**Notes & Troubleshooting**
- Confirm `data/train` and `data/test` exist and contain the original dataset files before running `transform_data.py`.
- If the notebook fails due to missing dependencies, double-check the PyTorch install step and system-specific GPU drivers.
- After successful training, `model.pth` will be created at the repository root and used by the API in `api/` for inference.

**Quick checklist**
- **Data**: `data/train` and `data/test` present — yes / no
- **Transforms**: Ran `transform_data.py` to generate `images/` and `annotations.csv` — yes / no
- **Dependencies**: Installed (including PyTorch) — yes / no
- **Notebook**: Ran from top to bottom and produced `model.pth` — yes / no
- **Env**: `.env.local` (local) or `.env.docker` (docker) populated — yes / no
- **Run**: `docker-compose up --build` starts services — yes / no

