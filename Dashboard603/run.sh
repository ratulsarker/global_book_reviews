#!/bin/bash

echo ""
echo "=========================================="
echo "📚 GOODBOOKS ANALYTICS PLATFORM"
echo "=========================================="
echo ""
echo "🚀 Starting dashboard..."
echo ""
echo "🌐 Dashboard will open at:"
echo "   → http://localhost:8501"
echo "   → http://127.0.0.1:8501"
echo ""
echo "💡 Press Ctrl+C to stop the server"
echo ""
echo "=========================================="
echo ""

# Run streamlit
streamlit run app.py

echo ""
echo "Dashboard stopped."
echo ""

