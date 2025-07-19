git add .
git commit -m "feat: src"
git push
rm -r catalog-output
python3 tools/catalog_apps.py
git add .
git commit -m "feat: catalog"
git push