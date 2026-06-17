from flask import Flask, render_template, request, send_file
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def home():

    df = pd.read_csv('data/students.csv')

    # Total
    df['Total'] = (
        df['Math']
        + df['Science']
        + df['English']
        + df['Social Science']
        + df['Hindi']
    )

    # Percentage
    df['Percentage'] = round((df['Total'] / 500) * 100, 2)

    # Grade
    def get_grade(p):
        if p >= 90:
            return 'A+'
        elif p >= 80:
            return 'A'
        elif p >= 70:
            return 'B'
        elif p >= 60:
            return 'C'
        else:
            return 'Fail'

    df['Grade'] = df['Percentage'].apply(get_grade)
    df['Status'] = df['Percentage'].apply(
    lambda x: 'Pass' if x >= 40 else 'Fail'
)

    # Rank on full data
    df = df.sort_values(by='Total', ascending=False)
    df['Rank'] = range(1, len(df) + 1)

    # Search
    search = request.args.get('search')

    if search:
        df = df[df['Name'].str.contains(search, case=False, na=False)]

    average_math = round(df['Math'].mean(), 2)
    highest_math = df['Math'].max()
    lowest_math = df['Math'].min()

    top_student = df.loc[df['Math'].idxmax()]['Name']

    highest_percentage = df['Percentage'].max()
    average_percentage = round(df['Percentage'].mean(), 2)

    total_students = len(df)

    print(df[['Name', 'Rank']].head(20))
    print(df.columns)

    ranking_data = df.values.tolist()

    return render_template(
        'index.html',
        average=average_math,
        highest=highest_math,
        lowest=lowest_math,
        total=total_students,
        top=top_student,
        ranking=ranking_data,
        highest_percentage=highest_percentage,
        average_percentage=average_percentage
    )
@app.route('/graph')
def graph():

    df = pd.read_csv('data/students.csv')

    # Create Total column
    df['Total'] = (
        df['Math']
        + df['Science']
        + df['English']
        + df['Social Science']
        + df['Hindi']
    )

    top10 = df.sort_values('Total', ascending=False).head(10)

    plt.figure(figsize=(10, 5))
    plt.bar(top10['Name'], top10['Total'])

    plt.title('Top 10 Students')
    plt.xlabel('Student Name')
    plt.ylabel('Total Marks')

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig('static/top10.png')
    plt.close()

    return render_template('graph.html')

@app.route('/download')
def download_file():
    return send_file('data/students.csv', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
