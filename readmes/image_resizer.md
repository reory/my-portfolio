
![Last Commit](https://img.shields.io/github/last-commit/reory/bulk_image_resizer?cacheSeconds=60)
![Repo Size](https://img.shields.io/github/repo-size/reory/bulk_image_resizer?cacheSeconds=60)
![License](https://img.shields.io/badge/License-MIT-green)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pillow](https://img.shields.io/badge/Pillow-60b5ff?style=for-the-badge&logo=python&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)

A high-performance Python tool for recursive image optimization.

---

# 🚀 Key Features

- **Multithreaded:** Uses `ThreadPoolExecutor` for batch processing.
- **LANCZOS Scaling:** High-quality resampling via `Pillow`.
- **Modular Logging:** Professional log tracking.
- **Progress Tracking:** Real-time visual feedback with `tqdm`.

---

## ⚒️ Setup

Clone the repository and install dependencies:
```bash
git clone [https://github.com/reory/bulk_image_resizer.git](https://github.com/reory/bulk_image_resizer.git)
cd bulk_image_resizer
bash
pip install -r requirements.txt
```
### Configure Paths
```
Open resizer.py and update your source and destination folders:
src = r"C:\Users\Admin\Desktop\Photos"
dest = r"C:\Users\Admin\Desktop\Optimized_Photos"
```
### Run
```bash
python resizer.py
```

---

# 🗺️ Future Roadmap Features
- [ ] CLI Support: Use argparse to pass paths and dimensions via terminal.

- [ ] Format Expansion: Add .webp and .webp support with auto-conversion.

- [ ] Efficiency Report: Calculate and log total "MB Saved" at session end.

- [ ] De-duplication: Use MD5 hashing to skip identical files and save time.

---

# Notes
Any issues with the code please feel free to reach out to me.
Cheers 😁

---

See [LICENSE.md](LICENSE.md) for usage rights and [CONTRIBUTING.md](CONTRIBUTING.md) for how to help.

---

* **Built by Roy Peters**
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Roy%20Peters-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/roy-p-74980b382/)
