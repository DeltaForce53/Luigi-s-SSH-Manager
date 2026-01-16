# Luigi-s-SSH-Manager
My personal ssh manager optimized for Windows.

A simple SSH Manager built in Python.

## Informations 

- It stores it database of connctions into a JSON file names `connections.json`
- You can make it a **.exe** file !

## How to make it a .exe file

```bash
cd ./Luigi-s-SSH-Manager
```

1. Create a virtual environment :

```python
python -m venv venv
```

2. Activate the virtual environment :

```python
venv\Scripts\activate
```

3. Install the required packages :

```python
pip install -r requirements.txt
```

4. Build the .exe file :

```python
pyinstaller --onefile --windowed ssh-manager.py
```
