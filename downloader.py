import requests
import threading
import os

def dmp_downloader(url, connection_num = 4 , cancel_flag=None):
    total_size, pieces_support = file_info(url)

    if not pieces_support:
        print("Server does not support multiple pieces! Downloading without dividing the file.")
        return
    
    pieces = calculate_pieces(total_size, connection_num)
    workers = []

    for i, (start,end) in enumerate(pieces):
        worker = threading.Thread(target=download_worker,args=(url,start,end,i,cancel_flag))
        workers.append(worker)
        worker.start()

        for worker in workers:
            worker.join()

    if cancel_flag and cancel_flag.is_set():
        print("\n [CLEANING] Deleting pieces")
        for i in range(connection_num):
            file = f"temp_part{i}.dmp"
            if os.path.exists(file):
                os.remove(file)
        return
    print(f"All workers did their job and pieces are written on the disc!")

    file_name = url.split('/')[-1]

    merge_files(file_name,connection_num)

def file_info(url):
    answer = requests.head(url, allow_redirects=True)

    size_byte = int(answer.headers.get('Content-Length',0))

    pieces_support = answer.headers.get('Accept-Ranges') == 'bytes'

    size_mb = size_byte / (1024*1024)

    print(f"Destination URL: {url}")
    print(f"File Size: {size_mb:.2f} MB")
    print(f"Pieced download support: {'Yes' if pieces_support else 'No'}")

    return size_mb, pieces_support

def calculate_pieces(total_size , connection_num = 4):
    piece_size = total_size / connection_num
    pieces = []

    for i in range(connection_num):
        start = int(i * piece_size)

        if i == connection_num-1:
            end = total_size -1 
        else:
            end = start + piece_size - 1
        
        pieces.append((start,end))
        print(f"Piece {i}: bytes={start}-{end}")
    
    return pieces

def download_worker(url,start,end,part_num,cancel_flag=None):
    headers={'Range' : f'bytes={start}-{end}'}
    print(f"Starting part {part_num} 's download ({start}-{end})...")

    response = requests.get(url,headers=headers,stream= True)

    fileName = f"temp_part_{part_num}.dmp"

    with open(fileName, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if cancel_flag and cancel_flag.is_set():
                print(f"Part {part_num} is cancelling.")
                return

            if chunk:
                file.write(chunk)
    
    print(f"Part {part_num} has been downloaded successfully & saved as {fileName}.")

def merge_files(target_file_name, connection_num=4):
    print(f"\n{target_file_name}'s pieces are merging...")

    with open(target_file_name, "wb") as main_file:
        for i in range(connection_num):
            piece_name= f"temp_part_{i}.dmp"

            with open(piece_name, "rb") as piece_file:
                main_file.write(piece_file.read())

            os.remove(piece_name)
            print(f"{piece_name} has been added to file and deleted.")

    print(f"\n File has been constructed and ready: {target_file_name}")
if __name__ == "__main__":
    test_url = "https://www.google.com"
    file_info(test_url)
    calculate_pieces(100)
