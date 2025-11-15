import csv
from googleapiclient.discovery import build

# Configuração da API do YouTube
API_KEY = "sua_chave"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Inicializar cliente da API
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

def get_channel_info(channel_id):
    """Coletar informações gerais do canal."""
    try:
        request = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        )
        response = request.execute()
        if "items" in response and response["items"]:
            channel = response["items"][0]
            return {
                "title": channel["snippet"]["title"],
                "channel_id": channel_id,
                "subscribers": channel["statistics"]["subscriberCount"],
                "views": channel["statistics"]["viewCount"],
                "videos": channel["statistics"]["videoCount"]
            }
        else:
            print(f"Erro: Nenhum dado encontrado para o channel_id {channel_id}")
            return None
    except Exception as e:
        print(f"Erro ao coletar dados do canal {channel_id}: {e}")
        return None

def get_videos(channel_id, max_results=100):
    """Listar vídeos mais visualizados do canal."""
    try:
        request = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=max_results,
            order="viewCount"  # Ordena por visualizações
        )
        response = request.execute()
        videos = []
        for item in response.get("items", []):
            if "videoId" in item["id"]:
                videos.append({
                    "title": item["snippet"]["title"],
                    "videoId": item["id"]["videoId"]
                })
        return videos
    except Exception as e:
        print(f"Erro ao coletar vídeos do canal {channel_id}: {e}")
        return []

def get_comments(video_id, max_results=100):
    """Coletar comentários de um vídeo específico."""
    try:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            textFormat="plainText"
        )
        response = request.execute()
        comments = []
        for item in response.get("items", []):
            top_comment = item["snippet"]["topLevelComment"]["snippet"]
            comments.append({
                "author": top_comment["authorDisplayName"],
                "comment": top_comment["textDisplay"],
                "likes": top_comment["likeCount"]
            })
        return comments
    except Exception as e:
        print(f"Erro ao coletar comentários do vídeo {video_id}: {e}")
        return []

def save_to_csv(filename, data, headers):
    """Salvar dados em um arquivo CSV."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

# IDs dos canais dos times
channel_ids = {
    "Athletico Paranaense": "UCUN1ASH969TSwnuUUU56TmA", #Athletico PR
    "Atlético Goianiense": "UCNhcUhri6NMKqzGju0QOUKg", #Atletico GO
    "Bahia": "UCcqRCjHozEb9CQHwf_cffdQ", #Bahia
    "Criciuma": "UC_ofom_8UQrjQJ28VqzitpQ", #Criciuma
    "Internacional": "UC7hAvFDWwVajRqrI86KCoxA", #Internacional
    "Fortaleza": "UCV5UiFF5AlNKW4sLXcYMG_g", #Fortaleza
    "São Paulo": "UCX3zTAsEoZ61rQMYb_08Tow", #Sao paulo
    "Corinthians": "UCqRraVICLr0asn90cAvkIZQ", #Corinthians
    "Vitoria": "UCT2ACrmb364amkLW8L8IhBA", #Vitoria
    "Gremio": "UCHKbUAiKHsWCCZrkDY_PZ8Q", #Gremio
    "Juventude": "UCrY4s3Eq7zSa5SE1LjoW_xg", #Juventude
    "Bragantino": "UC0x9Ypk2Z1lUdR4a88jMC2Q" #Bragantino
    
}

if __name__ == "__main__":
    # Tabela para informações gerais dos canais
    general_info_data = []
    general_info_headers = ["channel_name", "channel_id", "subscribers", "views", "videos"]

    for team, channel_id in channel_ids.items():
        print(f"Coletando dados para {team}...")
        
        # Coletar informações gerais do canal
        channel_info = get_channel_info(channel_id)
        if channel_info:
            general_info_data.append(channel_info)
            print("Informações do Canal:")
            print(channel_info)
        
        # Coletar vídeos mais visualizados
        print("\nColetando dados de vídeos e comentários...")
        videos = get_videos(channel_id)
        video_data = []
        for video in videos:
            video_info = {
                "video_title": video["title"],
                "video_id": video["videoId"]
            }
            
            # Coletar comentários do vídeo
            comments = get_comments(video["videoId"])
            for comment in comments:
                video_data.append({
                    "video_title": video["title"],
                    "video_id": video["videoId"],
                    "comment_author": comment["author"],
                    "comment_text": comment["comment"],
                    "comment_likes": comment["likes"]
                })
        
        # Salvar dados em tabelas separadas por time (vídeos e comentários)
        video_headers = ["video_title", "video_id", "comment_author", "comment_text", "comment_likes"]
        save_to_csv(f"{team}_videos_and_comments.csv", video_data, video_headers)
        print(f"Dados de vídeos e comentários do time {team} salvos em {team}_videos_and_comments.csv")
    
    # Salvar dados gerais dos canais em um único CSV
    save_to_csv("channels_general_info.csv", general_info_data, general_info_headers)
    print("Informações gerais dos canais salvas em channels_general_info.csv")
