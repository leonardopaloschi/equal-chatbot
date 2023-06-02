A parte do código relacionada a filtragem das páginas foi utiliado um modelo especifíco do Hugging Face chamado "distilbert-base-multilingual-cased-sentiments-student" por meio da biblioteca Transformers.

A linha de código que inicia o pipeline do classificador de sentimentos é a seguinte:

distilled_student_sentiment_classifier = pipeline(
    model="lxyuan/distilbert-base-multilingual-cased-sentiments-student", 
    return_all_scores=True
)
Nessa linha, estamos criando uma instância do pipeline do Hugging Face para o modelo "distilbert-base-multilingual-cased-sentiments-student". Esse modelo é baseado no algoritmo DistilBERT e foi treinado para realizar análise de sentimentos em texto em vários idiomas. Ao definir return_all_scores=True, estamos configurando o pipeline para retornar todas as pontuações de sentimentos possíveis, em vez de apenas o rótulo da classe mais provável.

Em seguida, o código realiza a análise de sentimento do conteúdo de uma página da web usando o pipeline que acabamos de criar:

distilled_student_sentiment_classifier_output = distilled_student_sentiment_classifier([soup.get_text().lower().replace('\n','').lstrip()])
Nessa linha, estamos chamando o pipeline distilled_student_sentiment_classifier passando o texto da página da web como entrada. O pipeline processa o texto e retorna as pontuações de sentimentos para o texto fornecido. As pontuações representam a probabilidade do texto pertencer a cada classe de sentimento (positivo, negativo, neutro, etc.).

Em seguida, o código insere a URL visitada, o conteúdo da página e a pontuação de sentimento na tabela 'webpages' do banco de dados:

cursor.execute("INSERT INTO webpages (url, content, sentiment) VALUES (?, ?, ?);", (url, soup.get_text().lower().replace('\n','').lstrip(), distilled_student_sentiment_classifier_output[0][0]['score']))
Aqui, estamos executando uma instrução SQL para inserir os valores na tabela 'webpages'. Os valores incluem a URL da página, o conteúdo da página após ser limpo (convertido para minúsculas e sem quebras de linha no início) e a pontuação de sentimento obtida do pipeline.

Depois disso foi necessário adicionar no comando !search a possibilidade de colocar o threshold.