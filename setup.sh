#!/bin/bash

echo "========================================="
echo "📚 GOODBOOKS DASHBOARD SETUP"
echo "========================================="
echo ""

# Check if we're in the right directory
if [ ! -d "Dashboard603" ]; then
    echo "❌ Error: Please run this script from the project_603 directory"
    exit 1
fi

# Step 1: Install Python dependencies
echo "📦 Step 1: Installing Python dependencies..."
cd Dashboard603
pip3 install -r requirements.txt --user
cd ..
echo "✅ Dependencies installed!"
echo ""

# Step 2: Check .env file
echo "⚙️  Step 2: Checking configuration..."
if [ ! -f "Dashboard603/.env" ]; then
    echo "📝 Creating .env file from template..."
    cp Dashboard603/.env.example Dashboard603/.env
    echo "⚠️  Please edit Dashboard603/.env and add your MySQL password!"
    echo "   Open: Dashboard603/.env"
    echo "   Change: MYSQL_PASSWORD=your_mysql_password_here"
    echo ""
fi
echo "✅ Configuration ready!"
echo ""

# Step 3: Check MySQL
echo "🗄️  Step 3: Checking MySQL server..."
if command -v mysql &> /dev/null; then
    echo "✅ MySQL found!"
    echo ""
    echo "📋 To load data into MySQL, you need to:"
    echo "   1. Start MySQL server"
    echo "   2. Run: mysql -u root -p < Analytical\\ SQL\\ Queries.sql"
    echo "   3. Or use MySQL Workbench to import the SQL file"
else
    echo "⚠️  MySQL not found in PATH"
    echo "   Make sure MySQL is installed and running"
fi
echo ""

# Step 4: Check Neo4j
echo "🕸️  Step 4: Checking Neo4j..."
echo "📋 To load Neo4j database:"
echo "   1. Install Neo4j Desktop"
echo "   2. Create a database named 'goodbooks'"
echo "   3. Stop the database"
echo "   4. Load dump file: goodbooks-2025-11-20T18-16-45.dump"
echo "   5. Start the database"
echo ""

# Final instructions
echo "========================================="
echo "✅ SETUP COMPLETE!"
echo "========================================="
echo ""
echo "📝 Next steps:"
echo "   1. Edit Dashboard603/.env with your passwords"
echo "   2. Load data into MySQL (see above)"
echo "   3. Load data into Neo4j (see above)"
echo "   4. Run: cd Dashboard603 && streamlit run app.py"
echo ""
echo "📖 For detailed instructions, see README.md"
echo ""

