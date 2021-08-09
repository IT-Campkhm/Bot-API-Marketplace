import os

API_TOKEN_NP = os.environ.get('API_TOKEN_NP')


URL_TRACKING_NP = 'https://api.novaposhta.ua/v2.0/json/documentsTracking'

HEADERS_NOVAPOSHTA = {
    'Content-Type': 'application/json',
    'Cookie': 'PHPSESSID=ondu5nedvd8h9qlnn4em9c6onb; YIICSRFTOKEN=812269c73980b05ed71934f5bf074673b9595151s%3A88%3A%22dzhyYkk2cnRjUUc1czczOHNLaEw4elk5OEN0V2hFTUffNboKXZnUUKgyFyALoqzNeaImGw7eQBlf6duSJNGyZQ%3D%3D%22%3B'
}