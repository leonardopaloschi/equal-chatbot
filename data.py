"""
Este módulo se conecta a um banco de dados MySQL de forma assíncrona usando aiomysql,
recupera dados da tabela 'webpages', escreve o conteúdo de uma coluna especificada
em um arquivo de texto e retorna os dados.
Funções:
- get_data: Conecta-se ao banco de dados, recupera dados da tabela 'webpages', escreve
  em um arquivo de texto e retorna os dados recuperados.

Dependências:
- asyncio: Para execução assíncrona.
- aiomysql: Para operações assíncronas com MySQL.
- aiofiles: Para operações assíncronas com arquivos.
"""

import asyncio
import aiomysql
import aiofiles

async def get_data():
    """
    Asynchronously connects to a MySQL database, retrieves data from the 'webpages' table,
    writes the content of the specified column to a text file, and returns the data.

    This function creates a connection pool to a MySQL database using aiomysql,
    retrieves all rows from the 'webpages' table, extracts the content from a
    specific column (assumed to be at index 2), and writes this content to 'output.txt'
    using aiofiles for asynchronous file operations.

    Returns:
        list: A list of strings containing the content of the specified column
              from the 'webpages' table.

    Raises:
        aiomysql.Error: If there is an issue with the database connection or queries.
        OSError: If there is an issue with file operations.
    """
    # Create a connection pool
    pool = await aiomysql.create_pool(
        host='localhost',
        port=3306,
        user='your_user',
        password='your_password',
        db='database',
        autocommit=True
    )

    texts = []

    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            # Retrieve data from the table
            await cursor.execute("SELECT * FROM webpages;")
            data = await cursor.fetchall()

            # Prepare data for output
            for row in data:
                texts.append(row[2])

    # Specify the output text file
    output_file = 'output.txt'

    # Write the data to the text file using aiofiles
    async with aiofiles.open(output_file, 'w') as file:
        for text in texts:
            await file.write(text + '\n')

    pool.close()
    await pool.wait_closed()

    print(f"The contents of the 'webpages' table have been written to '{output_file}'.")

    return texts

# Entry point
if __name__ == '__main__':
    asyncio.run(get_data())
