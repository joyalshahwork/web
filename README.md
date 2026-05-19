# 🧩 Customer Segmentation — Flask Web App
### A beginner-friendly conversion from terminal script → full web UI

---

## 📁 Project Structure

```
flask-segmentation/
│
├── app.py                  ← Flask application (routes, logic)
│
├── templates/
│   └── index.html          ← The web page (HTML + Jinja2)
│
├── static/
│   ├── css/style.css       ← All visual styling (responsive!)
│   └── js/main.js          ← Browser interactivity (fetch, DOM)
│
├── src/
│   ├── __init__.py
│   ├── preprocess.py       ← (unchanged from original)
│   ├── clustering.py       ← (unchanged from original)
│   └── visualize.py        ← (unchanged from original)
│
├── data/
│   └── mall_customers.csv  ← Dataset
│
└── requirements.txt
```

---

## 🚀 How to Run

### Step 1 – Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 – Start the server
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 3 – Open in browser
Visit: **http://localhost:5000**

---

## 🧠 What Changed from the Terminal Version?

| Terminal (`main.py`)               | Web (`app.py`)                          |
|------------------------------------|-----------------------------------------|
| `python main.py` to run            | Visit a URL in the browser              |
| `plt.show()` pops up a window      | Charts encoded as base64 images in HTML |
| `print()` shows results in console | Results rendered as HTML cards          |
| Hard-coded `N_CLUSTERS = 5`        | User adjusts a slider                   |
| No interactivity                   | Click button → page updates instantly   |

---

## 📚 Key Concepts for Learners

### Flask Routes
```python
@app.route("/")          # maps URL "/" to this function
def index():
    return render_template("index.html")
```

### Sending Data: Browser → Flask
```javascript
// JavaScript (browser side)
fetch("/analyze", {
  method: "POST",
  body: JSON.stringify({ n_clusters: 5 })
})
```
```python
# Python (Flask side)
n_clusters = request.json.get("n_clusters")
```

### Sending Data: Flask → Browser
```python
# Flask returns a dictionary as JSON
return jsonify({ "success": True, "elbow_img": "..." })
```
```javascript
// JavaScript reads it
const data = await response.json();
img.src = `data:image/png;base64,${data.elbow_img}`;
```

### Responsive CSS (mobile-friendly)
```css
/* Works on ALL screen sizes – auto adjusts columns */
.segment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
}

/* Only applies on screens ≥ 640px wide */
@media (min-width: 640px) {
  .btn-primary { width: auto; }
}
```

---

## 🔧 What to Try Next (Stretch Goals)

1. **Upload your own CSV** – add a `<input type="file">` and handle it in Flask
2. **Download segmented CSV** – add a `/download` route that sends the file
3. **Show a data preview table** – render the first 10 rows of the dataset
4. **Add a dark/light mode toggle** – use a CSS class + JS to switch themes
5. **Deploy to the web** – try Render.com or Railway.app (both free)
