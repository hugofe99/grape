# 🍇 Grape

## 📍 Getting started locally
```
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run src/frontend/main.py
```

## 🛣️ Roadmap
 - [ ] References timeline
 - [ ] Tests
 - [ ] Documentation
 - [x] Fix padding issue of graph
    > Handled graph as agraph component instead of pyvis html
 - [x] Migrate networkx to [streamlit-agraph](https://github.com/ChrisDelClea/streamlit-agraph?ref=blog.streamlit.io)?
    > Implemented PaperGraph method to export as agraph component
