from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# دالة لإنشاء قاعدة البيانات وجدول الرسائل إذا لم يكونوا موجودين
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, name TEXT, message TEXT)')
    conn.close()

# تشغيل الدالة فوراً لتجهيز قاعدة البيانات
init_db()

# مسار الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('home.html')

# مسار صفحة من نحن
@app.route('/about')
def about():
    return render_template('about.html')

# مسار صفحة اتصل بنا (يستقبل البيانات عبر POST)
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # سحب البيانات من النموذج
        name = request.form['name']
        message = request.form['message']
        
        # حفظ البيانات في قاعدة البيانات
        conn = sqlite3.connect('database.db')
        conn.execute('INSERT INTO messages (name, message) VALUES (?, ?)', (name, message))
        conn.commit()
        conn.close()
        
        # توجيه المستخدم لصفحة الشكر
        return redirect(url_for('thank_you'))
    
    # إذا كان الطلب GET، اعرض صفحة النموذج فقط
    return render_template('contact.html')

# مسار صفحة الشكر بعد الإرسال
@app.route('/thank-you')
def thank_you():
    return "<h2>شكراً لرسالتك! لقد تم حفظها بنجاح.</h2> <a href='/'>العودة للرئيسية</a>"

# مسار لعرض الرسائل (لوحة التحكم المصغرة)
@app.route('/messages')
def view_messages():
    # 1. الاتصال بقاعدة البيانات
    conn = sqlite3.connect('database.db')
    
    # 2. سحب كل البيانات من جدول الرسائل
    cursor = conn.execute('SELECT * FROM messages')
    all_messages = cursor.fetchall() # جلب كل الصفوف
    
    conn.close()
    
    # 3. إرسال البيانات إلى صفحة HTML لعرضها
    return render_template('messages.html', messages=all_messages)

if __name__ == '__main__':
    # تشغيل السيرفر
    app.run(debug=True)