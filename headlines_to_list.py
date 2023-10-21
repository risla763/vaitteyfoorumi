from markupsafe import escape
from database import db
from sqlalchemy import text

def headlines_list():
    sql = text("SELECT headline_text FROM headlines WHERE visible = TRUE")
    data = db.session.execute(sql)
    headlines = [headline[0] for headline in data.fetchall()]
    return headlines

def headline_ids_list():
    sql = text("SELECT headline_id FROM headlines WHERE visible = TRUE")
    data = db.session.execute(sql)
    headline_ids = [headline[0] for headline in data.fetchall()]
    return headline_ids

def opinions_list():
    result_list = []
    headlines = headlines_list()
    for i in headlines:
        sql = text("SELECT opinion FROM opinions WHERE headline = :headline")
        result = db.session.execute(sql, {"headline": i}).fetchall()
        for j in result:
            result_list.append((j))
    return result_list

def count_percentages():
    result_list = []
    headlines = headlines_list()
    for i in headlines:
        sql = text("SELECT headline, SUM(CASE WHEN answer = 'agree' THEN 1 ELSE 0 END) as agree_count, SUM(CASE WHEN answer = 'disagree' THEN 1 ELSE 0 END) as disagree_count FROM answers WHERE headline = :headline_text GROUP BY headline")
        result = db.session.execute(sql, {"headline_text": i}).fetchall()
        for j in result:
            result_list.append((j))
    return result_list

def combination(headlines,answers,opinions,headline_ids):
    combination_of_three = []
    for h, a, o, i in zip(headlines,answers,opinions,headline_ids):
        combination_of_three.append({'headline': h, 'agree_count': a[1], 'disagree_count': a[2], 'opinion':o[0],'id':i})
    return combination_of_three


