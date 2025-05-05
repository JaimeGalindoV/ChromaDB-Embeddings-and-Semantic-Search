import os

import chromadb
from chromadb.config import Settings

DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DIR, 'data')
chroma_client = chromadb.PersistentClient(path=DB_PATH, settings=Settings(allow_reset=True, anonymized_telemetry=False))
sample_collection = chroma_client.get_or_create_collection(name="JaimeGalindo_collection")

documents = [
    "Mars is known as the Red Planet due to its iron-rich soil and thin atmosphere.",
    "The Amazon Rainforest produces 20% of the Earth's oxygen and is home to millions of species.",
    "Artificial intelligence is revolutionizing industries like healthcare and finance through machine learning algorithms.",
    "Lionel Messi holds the record for most goals scored in a calendar year (91 goals in 2012).",
    "The Industrial Revolution began in Britain in the late 18th century, transforming manufacturing processes.",
    "Christopher Nolan's 'Inception' explores dream manipulation with groundbreaking visual effects.",
    "Regular exercise reduces the risk of chronic diseases like diabetes and heart conditions.",
    "Van Gogh's 'Starry Night' is a masterpiece of post-impressionist art, painted in 1889.",
    "Saturn's rings are composed primarily of ice particles and rocky debris.",
    "Photosynthesis converts sunlight into chemical energy, enabling plant growth.",
    "Quantum computing leverages qubits to solve complex problems exponentially faster than classical computers.",
    "The FIFA World Cup is the most-watched sporting event globally, with billions of viewers.",
    "The Great Wall of China spans over 13,000 miles and was built to protect against invasions.",
    "Pixar's 'Toy Story' (1995) was the first feature-length film made entirely with CGI.",
    "Mediterranean diets are linked to longevity and reduced risk of Alzheimer's disease.",
    "The Mona Lisa's enigmatic smile has fascinated art historians for centuries.",
    "Jupiter's Great Red Spot is a massive storm larger than Earth that has raged for over 350 years.",
    "Coral reefs support 25% of marine life but are threatened by ocean acidification.",
    "5G networks promise faster speeds and lower latency for connected devices.",
    "Usain Bolt holds the world record for the 100m sprint at 9.58 seconds.",
    "The Rosetta Stone, discovered in 1799, was key to deciphering Egyptian hieroglyphs.",
    "The 'Lord of the Rings' trilogy won 17 Academy Awards, a record for a fantasy series.",
    "Yoga improves flexibility, reduces stress, and enhances mental clarity.",
    "Banksy's street art combines social commentary with guerrilla-style installations.",
    "Neutron stars are so dense that a sugar-cube-sized amount weighs billions of tons.",
    "The Arctic permafrost stores vast amounts of methane, a potent greenhouse gas.",
    "Blockchain technology enables secure, decentralized transactions without intermediaries.",
    "Serena Williams has won 23 Grand Slam singles titles, the most in the Open Era.",
    "The invention of the printing press by Gutenberg in 1440 democratized knowledge.",
    "Stanley Kubrick's '2001: A Space Odyssey' redefined sci-fi cinema in 1968.",
    "Vitamin D from sunlight exposure is crucial for bone health and immune function.",
    "Michelangelo's David is a Renaissance sculpture symbolizing human perfection.",
    "Black holes warp spacetime so severely that not even light can escape them.",
    "Honeybees pollinate 70% of the world's crops, ensuring global food security.",
    "Augmented reality (AR) overlays digital information onto the physical world.",
    "Michael Phelps won 28 Olympic medals, the most in swimming history.",
    "The fall of the Berlin Wall in 1989 symbolized the end of the Cold War.",
    "Hayao Miyazaki's 'Spirited Away' is the highest-grossing film in Japanese history.",
    "Antioxidants in berries combat free radicals, slowing cellular aging.",
    "Frida Kahlo's self-portraits explore identity, pain, and Mexican culture.",
    "The James Webb Telescope observes infrared light to study early galaxies.",
    "Plastic pollution in oceans harms over 600 marine species annually.",
    "CRISPR gene-editing allows precise modifications to DNA sequences.",
    "The Tour de France covers 3,500 km over 21 stages in 23 days.",
    "The Magna Carta (1215) laid the foundation for modern constitutional law.",
    "Alfred Hitchcock's 'Psycho' pioneered the slasher genre with its iconic shower scene.",
    "Meditation reduces cortisol levels, lowering stress and anxiety.",
    "Jackson Pollock's drip paintings revolutionized abstract expressionism.",
    "Venus has a runaway greenhouse effect, making it the hottest planet in the solar system.",
    "Elephants communicate over long distances using infrasound vibrations.",
    "Self-driving cars use lidar and computer vision to navigate roads autonomously.",
    "The NBA's three-point line was introduced in 1979 to increase scoring variety."
]
metadatas = [{"category": "Space"},{"category": "Nature"},{"category": "Technology"},{"category": "Sports"},{"category": "History"},{"category": "Movies"},{"category": "Health"},{"category": "Art"},{"category": "Space"},{"category": "Nature"},{"category": "Technology"},{"category": "Sports"},{"category": "History"},{"category": "Movies"},{"category": "Health"},{"category": "Art"},{"category": "Space"},{"category": "Nature"},{"category": "Technology"},{"category": "Sports"},{"category": "History"},{"category": "Movies"},{"category": "Health"},{"category": "Art"},{"category": "Space"},{"category": "Nature"},{"category": "Technology"},{"category": "Sports"},{"category": "History"},{"category": "Movies"},{"category": "Health"},{"category": "Art"},{"category": "Space"},{"category": "Nature"},{"category": "Technology"},{"category": "Sports"},{"category": "History"},{"category": "Movies"},{"category": "Health"},{"category": "Art"},{"category": "Space"},{"category": "Nature"},{"category": "Technology"},{"category": "Sports"},{"category": "History"},{"category": "Movies"},{"category": "Health"},{"category": "Art"},{"category": "Space"},{"category": "Nature"},{"category": "Technology"},{"category": "Sports"}]

ids = ["1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52"]

sample_collection.add(documents=documents, metadatas=metadatas, ids=ids)

query_result = sample_collection.query(query_texts="Give me some facts about space", n_results=4)
result_documents = query_result["documents"][0]

for doc in result_documents:
    print(doc)
