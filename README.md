# VK Kendou - Documentation Complète

Bibliothèque Python puissante pour l'automatisation complète des interactions VK (VKontakte).

## Table des matières

- [Installation](#installation)
- [Configuration initiale](#configuration-initiale)
- [Gestion des sessions](#gestion-des-sessions)
- [Actions disponibles](#actions-disponibles)
- [Types d'URLs supportés](#types-durls-supportés)
- [Exemples d'utilisation](#exemples-dutilisation)
- [Gestion des erreurs](#gestion-des-erreurs)
- [Débogage](#débogage)
- [Structure des fichiers](#structure-des-fichiers)
- [Limitations et bonnes pratiques](#limitations-et-bonnes-pratiques)
- [Dépannage](#dépannage)

## Installation

```bash
pip install git+https://github.com/Ken56266325/vk_kendou.git
```

**Dépendances automatiques:**
- requests>=2.25.0
- beautifulsoup4>=4.9.0
- urllib3>=1.26.0

## Configuration initiale

### Code d'accès obligatoire

Chaque script utilisant VK Kendou DOIT contenir ce code d'accès :

```python
# CODE D'ACCÈS OBLIGATOIRE - NE JAMAIS SUPPRIMER
access_code =

import vk_kendou

# Créer le client
client = vk_kendou.Client()
```

**Sans ce code, la bibliothèque refusera de fonctionner avec l'erreur:**
```
❌ ERREUR D'AUTORISATION
Ce script n'est pas autorisé à utiliser cette bibliothèque.
Veuillez contacter le créateur du projet via:
📞 Téléphone: 0389561802
💬 Telegram: https://t.me/Kenny5626
```

## Gestion des sessions

### Créer une nouvelle session

```python
client = vk_kendou.Client()

# Méthode 1: Nom automatique
cookies = "remixsid=abc123; remixlang=0; remixdt=3600; ..."
result = client.dump_session(cookies)

if result["success"]:
    print(f"Session créée: {result['username']}_sessionvk.json")
    print(f"Username: {result['username']}")
    print(f"User ID: {result['user_id']}")
else:
    print(f"Erreur: {result['error']}")

# Méthode 2: Nom personnalisé
result = client.dump_session(cookies, "mon_compte_perso.json")
```

**Format des cookies VK:**
```
remixsid=1_ABC123...; remixlang=3; remixdt=0; remixnsid=vk1.a.XYZ...; remixgp=def456...; remixmvk-fp=789...
```

### Charger une session existante

```python
# Chargement automatique (premier compte trouvé)
result = client.load_session()

# Chargement manuel
result = client.load_session("username_sessionvk.json")

if result["success"]:
    print(f"Connecté: @{result['username']}")
    print(f"User ID: {result['user_id']}")
    print(f"Fichier: {result['session_file']}")
else:
    print(f"Erreur: {result['error']}")
```

### Gestion multi-comptes

```python
# Lister tous les comptes sauvegardés
accounts = client.list_saved_accounts()

print(f"{len(accounts)} comptes disponibles:")
for account in accounts:
    print(f"- {account['username']} (ID: {account['user_id']})")
    print(f"  Fichier: {account['file']}")

# Changer de compte
result = client.load_session("autre_compte_sessionvk.json")
```

## Actions disponibles

### 1. Like (❤️)

Supporte TOUS les types de contenu VK avec détection automatique :

```python
# Posts
result = client.like("https://vk.com/wall-191799800_12280")

# Photos (albums, profils, groupes)
result = client.like("https://vk.com/photo-123456_789")
result = client.like("https://vk.com/photo-123456_789?list=album456_789")

# Vidéos
result = client.like("https://vk.com/video-123456_789")

# Clips
result = client.like("https://vk.com/clip-123456_789")

# Commentaires
result = client.like("https://vk.com/wall-123456_789?reply=456")

# Vérification du résultat
if result["success"]:
    print(f"✅ Like ajouté sur {result['content_type']}")
    if result.get('post_id'):
        print(f"Post: {result['post_id']}")
    elif result.get('photo_id'):
        print(f"Photo: {result['photo_id']}")
    elif result.get('video_id'):
        print(f"Vidéo: {result['video_id']}")
else:
    print(f"❌ Échec: {result['error']}")
```

### 2. Commentaire (💬)

Supporte posts, photos, vidéos et clips :

```python
# Commentaire sur post
result = client.comment(
    "https://vk.com/wall-191799800_12280", 
    "Super publication! 👍"
)

# Commentaire sur photo
result = client.comment(
    "https://vk.com/photo526013438_457263969?list=album526013438_00",
    "Belle photo! ❤️"
)

# Commentaire sur vidéo
result = client.comment(
    "https://vk.com/video-123456_789",
    "Excellente vidéo!"
)

# Vérification
if result["success"]:
    print(f"✅ Commentaire ajouté: '{result['message']}'")
    print(f"Type: {result['content_type']}")
    if result.get('comment_id'):
        print(f"ID commentaire: {result['comment_id']}")
else:
    print(f"❌ Échec: {result['error']}")
```

### 3. Partage/Repost (🔄)

Disponible uniquement pour les posts :

```python
result = client.repost("https://vk.com/wall-191799800_12280")

if result["success"]:
    print(f"✅ Post partagé: {result['post_id']}")
else:
    print(f"❌ Échec: {result['error']}")
```

### 4. Follow/Add automatique (👥)

Détection automatique du type (utilisateur/groupe) :

```python
# Groupes/Communautés (abonnement automatique)
result = client.follow("https://vk.com/public123456")
result = client.follow("https://vk.com/club123456")
result = client.follow("https://vk.com/nom_groupe")

# Utilisateurs (ajout d'ami)
result = client.follow("https://vk.com/id123456")
result = client.follow("https://vk.com/nom_utilisateur")

# Vérification
if result["success"]:
    action = result["action"]
    if action == "follow_group":
        print(f"✅ Groupe suivi: {result['group_id']}")
    elif action == "add_friend":
        print(f"✅ Ami ajouté: {result['user_id']}")
    elif action == "already_member":
        print(f"ℹ️ Déjà membre du groupe")
    elif action == "already_friends":
        print(f"ℹ️ Déjà ami")
    elif action == "request_sent":
        print(f"✅ Demande envoyée (profil/groupe privé)")
else:
    print(f"❌ Échec: {result['error']}")
```

## Types d'URLs supportés

### URLs de contenu

```python
# Posts/Publications
"https://vk.com/wall-123456_789"
"https://vk.com/wall123456_789"
"https://m.vk.com/wall-123456_789"

# Photos
"https://vk.com/photo-123456_789"
"https://vk.com/photo526013438_457263969?list=album526013438_00"
"https://vk.com/album456_789?z=photo-123456_789"
"https://vk.com/public789?z=photo-123456_789"

# Vidéos
"https://vk.com/video-123456_789"
"https://vk.com/clip-123456_789"

# Commentaires (paramètre reply)
"https://vk.com/wall-123456_789?reply=456"
"https://m.vk.com/photo526013438_457263969?list=album526013438_00&reply=1746"
```

### URLs d'entités (utilisateurs/groupes)

```python
# Utilisateurs
"https://vk.com/id123456"
"https://vk.com/durov"
"https://vk.com/nom_utilisateur"

# Groupes/Communautés
"https://vk.com/public123456"
"https://vk.com/club123456"
"https://vk.com/apiclub"
"https://vk.com/nom_groupe"

# Versions mobiles (conversion automatique)
"https://m.vk.com/id123456"
"https://m.vk.com/public123456"
```

## Exemples d'utilisation

### Script basique

```python
# CODE D'ACCÈS OBLIGATOIRE
access_code = 

import vk_kendou

# Initialiser le client
client = vk_kendou.Client()

# Charger la session
result = client.load_session("mon_compte_sessionvk.json")
if not result["success"]:
    print(f"Erreur session: {result['error']}")
    exit()

print(f"Connecté: @{result['username']}")

# Actions simples
client.like("https://vk.com/wall-123456_789")
client.comment("https://vk.com/wall-123456_789", "Salut!")
client.repost("https://vk.com/wall-123456_789")
client.follow("https://vk.com/public123456")
```

### Bot automatisé avec gestion d'erreurs

```python
# CODE D'ACCÈS
access_code = 

import vk_kendou
import time
import random

client = vk_kendou.Client()

# Charger session avec vérification
result = client.load_session()
if not result["success"]:
    print(f"❌ Session: {result['error']}")
    cookies = input("Entrez vos cookies VK: ")
    result = client.dump_session(cookies)
    if not result["success"]:
        print(f"❌ Impossible de créer la session: {result['error']}")
        exit()

print(f"✅ Connecté: @{result['username']}")

# Liste d'URLs à traiter
urls = [
    "https://vk.com/wall-191799800_12280",
    "https://vk.com/photo-123456_789",
    "https://vk.com/video-456789_123"
]

# Messages de commentaires variés
messages = [
    "Super! 👍",
    "J'adore ❤️",
    "Excellent contenu!",
    "Merci pour le partage 🔥",
    "Bravo! 💯"
]

# Bot automatisé
for i, url in enumerate(urls, 1):
    print(f"\n📌 [{i}/{len(urls)}] Traitement: {url}")
    
    # Like
    like_result = client.like(url)
    if like_result["success"]:
        print(f"   ✅ Like: {like_result['content_type']}")
    else:
        print(f"   ❌ Like échoué: {like_result['error']}")
    
    # Commentaire (si applicable)
    if like_result.get("content_type") in ["post", "photo", "video", "clip"]:
        time.sleep(2)  # Pause entre actions
        
        message = random.choice(messages)
        comment_result = client.comment(url, message)
        
        if comment_result["success"]:
            print(f"   ✅ Commentaire: '{message}'")
        else:
            print(f"   ❌ Commentaire échoué: {comment_result['error']}")
    
    # Pause aléatoire entre URLs
    if i < len(urls):
        pause = random.uniform(3, 7)
        print(f"   ⏳ Pause {pause:.1f}s...")
        time.sleep(pause)

print("\n🎉 Bot terminé!")
```

### Gestionnaire multi-comptes

```python
# CODE D'ACCÈS
access_code =

import vk_kendou

client = vk_kendou.Client()
url_cible = "https://vk.com/wall-191799800_12280"

# Récupérer tous les comptes
accounts = client.list_saved_accounts()
print(f"📋 {len(accounts)} comptes disponibles")

# Action sur chaque compte
for account in accounts:
    print(f"\n👤 Compte: {account['username']}")
    
    # Charger le compte
    result = client.load_session(account['file'])
    if not result["success"]:
        print(f"   ❌ Chargement échoué: {result['error']}")
        continue
    
    # Like avec ce compte
    like_result = client.like(url_cible)
    if like_result["success"]:
        print(f"   ✅ Like ajouté par @{account['username']}")
    else:
        print(f"   ❌ Like échoué: {like_result['error']}")
    
    time.sleep(3)  # Pause entre comptes

print("\n✅ Actions terminées sur tous les comptes")
```

## Gestion des erreurs

Tous les résultats suivent ce format standard :

```python
# Succès
{
    "success": True,
    "content_type": "post",           # Type détecté
    "post_id": "wall-123456_789",     # ID du contenu
    "action": "like"                  # Action effectuée
}

# Échec
{
    "success": False,
    "error": "Message d'erreur détaillé"
}
```

### Types d'erreurs courantes

```python
# Erreurs de session
{"error": "Session non chargée. Utilisez load_session() d'abord."}
{"error": "Session VK expirée, veuillez vous reconnecter"}
{"error": "Access token manquant"}

# Erreurs de contenu
{"error": "Impossible d'analyser ce contenu"}
{"error": "Type de contenu non supporté: audio"}
{"error": "Hash de réaction manquant"}

# Erreurs d'API VK
{"error": "Erreur API: User authorization failed"}
{"error": "Publication introuvable"}
{"error": "Commentaires désactivés"}
{"error": "Limite de commentaires atteinte"}

# Erreurs réseau
{"error": "Erreur HTTP: 404"}
{"error": "Erreur HTTP: 403"}
```

### Gestion robuste des erreurs

```python
def action_securisee(client, action_func, *args):
    """Wrapper sécurisé pour les actions VK"""
    try:
        result = action_func(*args)
        
        if result["success"]:
            return True, result
        else:
            error = result["error"]
            
            # Gestion spéciale selon le type d'erreur
            if "session" in error.lower() or "expirée" in error.lower():
                print("🔄 Session expirée - rechargement nécessaire")
                return False, "session_expired"
            elif "limite" in error.lower() or "limit" in error.lower():
                print("⚠️ Limite atteinte - pause recommandée")
                return False, "rate_limited"
            else:
                print(f"❌ Erreur: {error}")
                return False, error
                
    except Exception as e:
        print(f"💥 Exception: {e}")
        return False, str(e)

# Utilisation
success, result = action_securisee(client, client.like, "https://vk.com/wall-123_456")

if success:
    print("✅ Action réussie")
elif result == "session_expired":
    # Recharger la session
    client.load_session("nouvelle_session.json")
elif result == "rate_limited":
    # Faire une pause
    time.sleep(3600)  # 1 heure
```

## Débogage

### Mode debug détaillé

```python
def debug_action(client, action_name, action_func, *args):
    """Fonction de débogage pour les actions VK"""
    print(f"🔍 Debug {action_name}")
    print(f"Arguments: {args}")
    
    result = action_func(*args)
    
    print(f"Résultat complet:")
    for key, value in result.items():
        print(f"  {key}: {value}")
    
    return result

# Utilisation
result = debug_action(client, "LIKE", client.like, "https://vk.com/wall-123_456")
result = debug_action(client, "COMMENT", client.comment, "https://vk.com/wall-123_456", "Test")
```

### Logs détaillés des sessions

```python
def debug_session(client):
    """Affichage détaillé des informations de session"""
    print("🔍 INFORMATIONS DE SESSION")
    print(f"Username: {client.username}")
    print(f"User ID: {client.user_id}")
    print(f"Access Token: {client.access_token[:20] if client.access_token else 'None'}...")
    print(f"Session File: {client.session_file}")
    print(f"Cookies: {len(client.session.cookies.items())} cookies chargés")
    
    # Test de connectivité
    test_result = client.like("https://vk.com/wall-1_1")  # URL test
    print(f"Test connectivité: {'✅ OK' if test_result['success'] or 'introuvable' in test_result['error'] else '❌ Problème'}")

# Utilisation
debug_session(client)
```

### Analyse d'URL

```python
def debug_url(client, url):
    """Analyse détaillée d'une URL VK"""
    print(f"🔍 ANALYSE URL: {url}")
    
    # Test de détection de type
    from vk_kendou.utils import URLAnalyzer
    url_type, groups = URLAnalyzer.detect_url_type(url)
    
    print(f"Type détecté: {url_type}")
    print(f"Groupes extraits: {groups}")
    
    # Test d'extraction de contenu
    content_info = client._extract_content_info(url)
    if content_info:
        print("Informations extraites:")
        for key, value in content_info.items():
            print(f"  {key}: {value}")
    else:
        print("❌ Impossible d'extraire les informations")

# Utilisation
debug_url(client, "https://vk.com/wall-191799800_12280")
```

## Structure des fichiers

### Fichiers de session

Format: `{username}_sessionvk.json`

```json
{
  "username": "durov",
  "user_id": "1",
  "access_token": "vk1.a.ABC123...",
  "cookies": {
    "remixsid": "1_ABC123...",
    "remixlang": "3",
    "remixdt": "0",
    "remixnsid": "vk1.a.XYZ..."
  },
  "last_updated": 1758802390
}
```

### Fichiers générés automatiquement

```
votre_projet/
├── script.py                    # Votre script
├── durov_sessionvk.json         # Session utilisateur "durov"
├── user123_sessionvk.json       # Session utilisateur "user123"
├── groupe_admin_sessionvk.json  # Session utilisateur "groupe_admin"
└── device.json                  # Informations device (auto-généré)
```

### Gestion des fichiers

```python
import os
import glob

# Lister tous les fichiers de session
session_files = glob.glob("*_sessionvk.json")
print(f"Fichiers de session trouvés: {session_files}")

# Nettoyer les anciennes sessions
for file in session_files:
    age_days = (time.time() - os.path.getmtime(file)) / 86400
    if age_days > 30:  # Plus de 30 jours
        print(f"Session expirée: {file}")
        # os.remove(file)  # Décommenter pour supprimer

# Backup des sessions importantes
import shutil
important_sessions = ["admin_sessionvk.json", "main_account_sessionvk.json"]
for session in important_sessions:
    if os.path.exists(session):
        backup_name = f"backup_{session}"
        shutil.copy2(session, backup_name)
        print(f"Backup créé: {backup_name}")
```

## Limitations et bonnes pratiques

### Limites VK officielles

```python
# Recommandations quotidiennes
LIMITS = {
    "likes_per_day": 1000,
    "comments_per_day": 100,
    "friend_requests_per_day": 50,
    "group_joins_per_day": 20,
    "reposts_per_day": 50
}

# Cooldowns recommandés
COOLDOWNS = {
    "between_likes": (2, 5),        # 2-5 secondes
    "between_comments": (5, 10),    # 5-10 secondes  
    "between_follows": (10, 15),    # 10-15 secondes
    "between_accounts": (30, 60),   # 30-60 secondes
}
```

### Bonnes pratiques d'utilisation

```python
import time
import random

def safe_action(action_func, *args, cooldown=(2, 5)):
    """Action sécurisée avec cooldown aléatoire"""
    result = action_func(*args)
    
    # Pause aléatoire
    pause = random.uniform(*cooldown)
    time.sleep(pause)
    
    return result

# Utilisation
def bot_likes_securise(client, urls):
    """Bot de likes sécurisé"""
    success_count = 0
    
    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] Like: {url}")
        
        result = safe_action(client.like, url, cooldown=(3, 7))
        
        if result["success"]:
            success_count += 1
            print(f"   ✅ Succès")
        else:
            print(f"   ❌ Échec: {result['error']}")
            
            # Pause plus longue en cas d'erreur
            if "limite" in result["error"].lower():
                print("   ⚠️ Limite atteinte - pause 1h")
                time.sleep(3600)
    
    print(f"\n📊 Résultats: {success_count}/{len(urls)} likes réussis")
    return success_count

# Utilisation
urls_a_liker = [
    "https://vk.com/wall-123_456",
    "https://vk.com/photo-456_789",
    "https://vk.com/video-789_123"
]

bot_likes_securise(client, urls_a_liker)
```

### Rotation de comptes automatique

```python
def bot_multi_comptes(urls_cibles, action_per_account=10):
    """Bot avec rotation automatique des comptes"""
    client = vk_kendou.Client()
    accounts = client.list_saved_accounts()
    
    if not accounts:
        print("❌ Aucun compte disponible")
        return
    
    print(f"🔄 Rotation sur {len(accounts)} comptes")
    
    for account in accounts:
        print(f"\n👤 Compte: {account['username']}")
        
        # Charger le compte
        result = client.load_session(account['file'])
        if not result["success"]:
            print(f"   ❌ Chargement échoué")
            continue
        
        # Actions limitées par compte
        account_actions = 0
        for url in urls_cibles:
            if account_actions >= action_per_account:
                print(f"   ⚠️ Limite de {action_per_account} actions atteinte")
                break
            
            result = client.like(url)
            if result["success"]:
                account_actions += 1
                print(f"   ✅ [{account_actions}] Like ajouté")
            else:
                print(f"   ❌ Échec: {result['error']}")
            
            time.sleep(random.uniform(3, 6))
        
        print(f"   📊 {account_actions} actions effectuées")
        
        # Pause entre comptes
        time.sleep(random.uniform(30, 60))

# Utilisation
urls = ["https://vk.com/wall-123_456", "https://vk.com/wall-456_789"]
bot_multi_comptes(urls, action_per_account=5)
```

## Dépannage

### Problèmes de session

**Problème:** "Session non chargée"
```python
# Solution
client.load_session("votre_fichier_sessionvk.json")

# Vérifier l'existence du fichier
import os
if not os.path.exists("votre_fichier_sessionvk.json"):
    print("Fichier introuvable - créer une nouvelle session")
    cookies = input("Entrez vos cookies: ")
    client.dump_session(cookies, "votre_fichier_sessionvk.json")
```

**Problème:** "Session VK expirée"
```python
# Solution: Nouveau dump avec cookies frais
cookies_fresh = input("Cookies VK mis à jour: ")
result = client.dump_session(cookies_fresh)
if result["success"]:
    print(f"Session mise à jour: {result['filename']}")
```

### Problèmes d'actions

**Problème:** "Hash de réaction manquant"
```python
# Causes possibles:
# 1. URL invalide ou contenu supprimé
# 2. Permissions insuffisantes
# 3. Contenu dans un groupe privé

# Solution: Vérifier l'URL manuellement
url_test = "https://vk.com/wall-123456_789"
print("Vérifiez que cette URL est accessible dans votre navigateur")

# Tester avec une URL publique connue
result = client.like("https://vk.com/wall-1_1")  # Post public VK officiel
```

**Problème:** "Commentaires désactivés"
```python
# Solutions:
# 1. Vérifier les paramètres du post
# 2. Essayer sur un autre contenu
# 3. Tenter un like au lieu d'un commentaire

result = client.like(url)  # Alternative au commentaire
```

### Problèmes de détection

**Problème:** "Type de contenu non supporté"
```python
# Debug de l'URL
def debug_content_type(client, url):
    from vk_kendou.utils import URLAnalyzer
    
    print(f"URL analysée: {url}")
    url_type, groups = URLAnalyzer.detect_url_type(url)
    print(f"Type détecté: {url_type}")
    print(f"Groupes: {groups}")
    
    # Types supportés
    supported_types = [
        'wall_post', 'photo_simple', 'photo_z', 
        'video', 'clip', 'wall_comment'
    ]
    
    if url_type in supported_types:
        print("✅ Type supporté")
    else:
        print("❌ Type non supporté")
        print(f"Types supportés: {supported_types}")

debug_content_type(client, "votre_url_problematique")
```

### Problèmes de réseau

**Problème:** "Erreur HTTP 403/404/500"
```python
# Solutions par code d'erreur
def handle_http_error(error_code):
    solutions = {
        403: "Accès refusé - vérifier les permissions/session",
        404: "Contenu introuvable - URL invalide ou supprimé", 
        500: "Erreur serveur VK - réessayer plus tard",
        429: "Trop de requêtes - ralentir les actions"
    }
    
    return solutions.get(error_code, "Erreur inconnue")

# Test de connectivité
def test_connectivity(client):
    test_urls = [
        "https://vk.com/wall-1_1",      # Post public VK
        "https://vk.com/photo-1_1",     # Photo publique
        "https://vk.com/public1"        # Groupe public
    ]
    
    for url in test_urls:
        result = client.like(url)
        status = "✅" if result["success"] or "introuvable" in result["error"] else "❌"
        print(f"{status} {url}: {result.get('error', 'OK')}")

test_connectivity(client)
```

### Diagnostic complet

```python
def diagnostic_complet(client):
    """Diagnostic complet du client VK Kendou"""
    print("🔍 DIAGNOSTIC VK KENDOU")
    print("=" * 50)
    
    # 1. Vérifier la session
    print("\n📋 SESSION:")
    if client.username:
        print(f"✅ Username: {client.username}")
        print(f"✅ User ID: {client.user_id}")
        print(f"✅ Session file: {client.session_file}")
        
        if client.access_token:
            print(f"✅ Access token: présent ({len(client.access_token)} chars)")
        else:
            print("⚠️ Access token: absent")
    else:
        print("❌ Aucune session chargée")
        return
    
    # 2. Vérifier les cookies
    print(f"\n🍪 COOKIES:")
    cookie_count = len(client.session.cookies.items())
    print(f"✅ {cookie_count} cookies chargés")
    
    important_cookies = ['remixsid', 'remixnsid', 'remixgp']
    for cookie_name in important_cookies:
        cookie_value = client.session.cookies.get(cookie_name)
        if cookie_value:
            print(f"✅ {cookie_name}: présent")
        else:
            print(f"⚠️ {cookie_name}: absent")
    
    # 3. Test de connectivité
    print(f"\n🌐 CONNECTIVITÉ:")
    test_url = "https://vk.com/wall-1_1"
    result = client.like(test_url)
    
    if result["success"]:
        print("✅ Connexion VK: OK")
    elif "introuvable" in result["error"] or "not found" in result["error"]:
        print("✅ Connexion VK: OK (réponse valide)")
    else:
        print(f"❌ Connexion VK: {result['error']}")
    
    # 4. Vérifier les comptes disponibles
    print(f"\n👥 COMPTES:")
    accounts = client.list_saved_accounts()
    print(f"✅ {len(accounts)} comptes sauvegardés")
    
    for account in accounts[:3]:  # Afficher 3 premiers
        print(f"   • {account['username']} (ID: {account['user_id']})")
    
    if len(accounts) > 3:
        print(f"   ... et {len(accounts) - 3} autres")
    
    # 5. Recommandations
    print(f"\n💡 RECOMMANDATIONS:")
    
    if cookie_count < 10:
        print("⚠️ Peu de cookies - session potentiellement incomplète")
    
    if not client.access_token:
        print("⚠️ Pas d'access token - fonctions API limitées")
    
    if len(accounts) < 2:
        print("💡 Ajoutez des comptes multiples pour plus de robustesse")
    
    print("\n✅ Diagnostic terminé")

# Utilisation
diagnostic_complet(client)
```

## Support et contact

Pour toute question technique ou problème avec VK Kendou :

**Créateur du projet :**
- **Téléphone :** 0389561802
- **Telegram :** https://t.me/Kenny5626

**Informations importantes :**
- Version actuelle : 1.0.0
- Compatible Python : 3.7+
- Plateformes supportées : Windows, Linux, macOS, Android (Termux)

**Avant de contacter le support :**
1. Vérifiez que le code d'accès est présent dans votre script
2. Executez le diagnostic complet ci-dessus
3. Testez avec une URL VK publique connue
4. Vérifiez que vos cookies VK sont récents (< 24h)

La bibliothèque VK Kendou est conçue pour être robuste et facile à utiliser. Suivez cette documentation pour une utilisation optimale !
