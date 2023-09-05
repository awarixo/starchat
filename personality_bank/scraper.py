#%%
import requests
import re
from bs4 import BeautifulSoup
import os
# #%% The dwayne_johnson - Talks Interview
# url = "https://the-talks.com/interview/dwayne-johnson/"

# response= requests.get(url=url)
# soup = BeautifulSoup(response.text, 'html.parser')
# # print(soup.text)
# content= soup.find('div', class_="interview__content")
# questions = content.find_all('p', class_='q')
# answers = content.find_all('p', class_='a')

# for question, answer in zip(questions,answers):
#     question_text = question.get_text(strip=True)
#     answer_text = answer.get_text(strip=True)

#     interaction = f"# {question_text}\n{answer_text}\n\n"
#     interaction = interaction.replace("’", "\'")
#     interaction = interaction.replace("”", "\"")
#     interaction = interaction.replace("“", "\"")

#     try:
#         with open("personality_bank/dwayne_johnson1.txt", 'a') as doc:
#             doc.write(interaction)
#         # print(document)
#     except:
#         with open("personality_bank/dwayne_johnson1.txt", 'w') as doc:
#             doc.write(interaction)

#%% The dwayne_johnson - CNN Interview
# url = "https://edition.cnn.com/2021/12/29/entertainment/dwayne-the-rock-johnson-interview/index.html"
# questions=[]
# answers=[]

# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'html.parser')
# content = soup.find('div', class_="article__content")
# interactions = content.find_all('p', class_="paragraph inline-placeholder")
# # print(interactions)
# interactions = interactions[5:]
# print(interactions)

# for interaction in interactions:
#     if interaction.find("strong") is not None:
#         question = interaction.get_text(strip=True)
#         questions.append(question)
#     else:
#         answer =  interaction.get_text(strip=True)
#         answers.append(answer)

# for question, answer in zip(questions,answers):
#     interaction = f"# {question}\n{answer}\n\n"
#     interaction = interaction.replace("’", "\'")
#     interaction = interaction.replace("”", "\"")
#     interaction = interaction.replace("“", "\"")

#     # if os.path.exists("personality_bank/dwayne_johnson2.txt"):
#     try:
#         with open("personality_bank/dwayne_johnson2.txt", 'a') as doc:
#             doc.write(interaction)
#         # print(document)
#     except:
#         with open("personality_bank/dwayne_johnson2.txt", 'w') as doc:
#             doc.write(interaction)
#     # else: 
#     #     print("doesnt exist")
#     #     with open("personality_bank/dwayne_johnson2.txt", 'w') as doc:
#     #         doc.write(interaction)
# %%
url = "https://www.esquire.com/entertainment/interviews/a36037/dwayne-johnson-the-rock-0815/"
answers_text=[]
questions_text=[]

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
content = soup.find('div', class_="article-body-content article-body standard-body-content css-woto36 ewisyje7")
answers = content.find_all('p')
answers=answers[1:]
# del answers[]
for a in answers:
    answers_text.append(a.text)
print(f"answers_text[9]: {answers_text[9]}")
answers_text[9] = answers_text[9] + answers_text[10]
print(f"answers_text[9]: {answers_text[9]}")
del answers_text[3],answers_text[10]

questions = content.find_all('h2')
for q in questions:
    questions_text.append(q.text)
print(f"answers_text: {len(answers_text)}, questions_text: {len(questions_text)}")
for i,(q,a) in enumerate(zip(questions_text, answers_text)):

    print(f"Question{i}: {q}")
    print(f"Answer{i} : {a}\n")

    interaction = f"# {q}\n{a}\n\n"
    try:
        with open("personality_bank/dwayne_johnson.txt", 'a') as doc:
            doc.write(interaction)
        # print(document)
    except:
        with open("personality_bank/dwayne_johnson.txt", 'w') as doc:
            doc.write(interaction)




# %%

