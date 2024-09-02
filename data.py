import asyncio
import aiomysql
import aiofiles

async def get_data():
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
