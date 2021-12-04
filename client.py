import requests

dns = input("DNS LOAD BALANCER: ")


verbo = input('Verbo: ')


if verbo == "GET":
    get = requests.get('http://'+dns+':80/tasks/all_tasks/')
    print(get)
    print(get.json())

if verbo == "POST":

    titulo = input("Titulo: ")
   
    descricao = input("Descricao: ")

    post = requests.post('http://'+dns+':80/tasks/post/',
                        data={
                            'title': titulo, 
                            'pub_date': "2021-11-01T11:11:11Z", 
                            'description': descricao
                            }
                    )

    print(post)
    print(post.json())


if verbo == "DELETE":
    pk = input("Numero do delete: ")
    delete = requests.delete('http://'+dns+':80/tasks/tasks/'+pk)
    print(delete)
    print(delete.json())

