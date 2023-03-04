import json

# retorna os dados de similarity em formato de uma matriz quadrada


def open_similarity(path):

    arq = open(path, 'r')
    lines = arq.readlines()
    arq.close()

    similarity_data = list()
    for line in lines:
        line = line.rstrip()
        similarity_data.append(line.split())

    return similarity_data

# retorna uma lista contendo todos os nomes dos orientadore


def open_orientadores(path, len_projects, orientadores_list):

    orientadores_data = list()
    orientadores = list()
    with open(path) as file:
        orientadores_data = json.load(file)
        orientadores_list.append(orientadores_data)
        len_projects.append(len(orientadores_data))
        for data in orientadores_data:
            orientadores.append(data["Orientador:"])

    orientadores = list(set(orientadores))
    file.close()
    return orientadores


def main():
    path_similarity = "../SimilaridadesOrientadores/similarityOrientadores14.txt"
    path_orientadores = "resumoOrientadores/resumoOrientadores14.json"
    path_instance = "instance14.txt"
    orientadores_list = list()  # Contém todos os dados dos orientadores
    similarity_data = open_similarity(path_similarity)
    len_projects = list()

    orientadores_data = open_orientadores( path_orientadores, len_projects, orientadores_list)
    # Contém o dicionario dos orientadores
    orientadores_dic = orientadores_list[0] #Todo o arquivo json de orientadores

    arq = open(path_instance, 'w')

    line = str(len(orientadores_data)) + ' ' + str(len_projects[0]) + '\n'
    arq.write(line)

    # Criação da instancia para inviablizar pesos para trabalhos do mesmo orientador, caso forem o mesmo, temos -1 como peso
    # Além disso, precisamos criar uma matriz orientadores X Trabalhos, contendo suas similaridades, vamos analisar qual a melhor matriz similaridade de determinado orientador
    # E usá-la como o peso para o algoritmo

    orientadores_visitados = list()
    i = 0
    
    
    # Orientadores_dic representa todo o arquivo json, então vamos andar por todas as "instancias" de orientadores, que seriam todos os seus trabalhos e adicionar a uma lista daquele orientador ja visitado
    # Após isso, percorremos a matriz quadrada de similaridade, verificando qual linha representa ao orientador adicionado a lista, achado a sua linha, calculamos a media aritmetica daquela linha de similaridade
    # Verifica se é maior do que a antiga e atualiza. Fazemos isso com todas as "instancias" do mesmo orientador para achar a sua melhor similaridade, após isso com a linha de melhor similaridade encontrada
    # Percorremos novamente a matriz, verificando se o trabalho da coluna é do mesmo orientador, para indicar que é viável alocar ele naquele trabalho e então adicionamos no arquivo de instancia
    # o loop continua até que todos os orientadores sejam varridos. Criando assim, uma matriz orientador x similaridade
    while (i < len(orientadores_dic)):
        
        if orientadores_dic[i]['Orientador:'] not in orientadores_visitados:
            orientadores_visitados.append(orientadores_dic[i]['Orientador:'])
            media = 0
            indice_maior_media = 0
            maior_media = -1

            #Acha a melhor linha de similaridade do orientador anterior
            for j in range(len(similarity_data)):

                if orientadores_dic[j]["Orientador:"] == orientadores_dic[i]["Orientador:"]:
                        
                    for k in range(len(similarity_data[j])):
                        media += float(similarity_data[j][k])
                    media /= len(similarity_data[j])

                    if media > maior_media:
                        maior_media = media
                        indice_maior_media = j
            # Armazena a melhor linha do orientador no arquivo de instancia
            for j in range(len(similarity_data[indice_maior_media])):
                # Se o orientador da linha for o mesmo da coluna, então -1 para indicar que o trabalho é inviável
                if orientadores_dic[indice_maior_media]["Orientador:"] == orientadores_dic[j]["Orientador:"]:
                    similarity_data[indice_maior_media][j] = "-1"

                if j == len(similarity_data[indice_maior_media]) - 1:
                    line = str(similarity_data[indice_maior_media][j]) + '\n'
                else:
                    line = str(similarity_data[indice_maior_media][j]) + ' '
                arq.write(line)
    
        i += 1
        
        
              

    
    arq.close()         

        


    
    return 0













if __name__== "__main__":
    main()