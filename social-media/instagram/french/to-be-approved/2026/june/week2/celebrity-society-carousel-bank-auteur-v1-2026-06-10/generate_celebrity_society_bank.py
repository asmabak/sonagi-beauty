from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "launch-carousel-bank-auteur-v1-2026-06-10" / "generate_launch_bank.py"

spec = importlib.util.spec_from_file_location("launch_bank", BASE)
bank = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bank)

IMG = bank.IMG
DIA = bank.DIA
IRIS = bank.IRIS
MEDIA = Path.home() / "sonagi-beauty/media/reference visuals"

bank.ROOT = ROOT
bank.decks = [
    {
        "slug": "01-jennie-glass-skin-minimaliste",
        "label": "routine star",
        "title": "Jennie prouve que la glass skin n'a pas besoin de dix produits",
        "note": "Celebrity routine: Jennie. Source: Sonagi Reference celebrity article.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/celebrities/fr/jennie/",
        "slides": [
            {"bg": IMG/"celebrities/jennie-card-v3.webp", "wide_ok": True, "kicker": "K-pop skin", "title": "Jennie n'a pas une routine compliquée. Elle a une routine répétée.", "body": "Baume, toner calmant, outil. Le reste, c'est surtout de la constance."},
            {"bg": MEDIA/"Double Cleansing body.png", "wide_ok": True, "kicker": "Geste 1", "title": "Le baume fait tomber la journée.", "body": "SPF, pollution, maquillage: on retire d'abord le film, sur peau sèche, sans faire crisser la barrière.", "visual": DIA/"double-cleansing-mechanism.webp"},
            {"bg": MEDIA/"sonagib_Editorial_beauty_campaign_close-up_Asian_woman_applyi_ca84d377-dfc8-44bd-a361-cfda4b9995cf_1.png", "kicker": "Geste 2", "title": "Le toner vert calme avant de traiter.", "body": "Heartleaf n'est pas spectaculaire. Il rend la peau moins nerveuse, donc plus lumineuse."},
            {"bg": MEDIA/"glass_skin1.png", "wide_ok": True, "kicker": "Geste 3", "title": "L'outil ne remplace pas le soin. Il installe le rituel.", "body": "Trois minutes, toujours dans le même sens. Drainage léger, visage moins froissé le matin."},
            {"bg": MEDIA/"sonagib_Editorial_K-beauty_close-up_of_a_strikingly_beautiful_79e20c51-432e-49b5-a95f-b5fb0e377323_1.png", "wide_ok": True, "kicker": "La leçon", "title": "Trois étapes tenues battent dix étapes abandonnées.", "body": "La glass skin se construit plus par répétition que par accumulation."},
            {"bg": MEDIA/"beauty of joseon spf cream.jpg", "wide_ok": True, "kicker": "À copier", "title": "Baume le soir. Toner aux paumes. SPF le matin.", "body": "C'est moins excitant qu'une étagère pleine. C'est plus probable que tu le tiennes."},
            {"bg": MEDIA/"sonagib_Editorial_K-beauty_close-up_of_a_strikingly_beautiful_85c22752-a8e3-42f1-8307-7b4c35e56cbd_0.png", "wide_ok": True, "kicker": "À faire", "title": "Copie la logique, pas la célébrité.", "body": "Tag boutique à connecter. Quiz routine dans la bio. Article complet sur Sonagi Reference."},
        ],
    },
    {
        "slug": "02-hailey-glazed-donut-kbeauty",
        "label": "glazed skin",
        "title": "Hailey a rendu le glow viral. La K-beauty l'avait déjà codé.",
        "note": "Celebrity routine: Hailey Bieber. Source: Sonagi Reference celebrity article.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/celebrities/fr/hailey-bieber/",
        "slides": [
            {"bg": IMG/"celebrities/hailey-bieber-hero-v3.webp", "wide_ok": True, "kicker": "Glazed donut", "title": "Le glazed donut n'est pas une invention. C'est une traduction.", "body": "Dewy, glass skin, mool-gwang: quatre mots pour une peau qui retient l'eau."},
            {"bg": MEDIA/"model_general_european-brunette_BoJ_sunscreen_v1.png.jpg", "wide_ok": True, "kicker": "Base", "title": "Sans SPF, pas de glow durable.", "body": "Le fini dewy commence souvent par une crème solaire qui se fond sans blanchir."},
            {"bg": MEDIA/"glass_skin3.png", "wide_ok": True, "kicker": "Surface", "title": "Le glow est une question d'optique.", "body": "Quand la surface est hydratée et régulière, la lumière glisse au lieu d'accrocher.", "visual": DIA/"glass-skin-mechanism.webp"},
            {"bg": MEDIA/"sonagib_Editorial_K-beauty_close-up_of_a_strikingly_beautiful_85c22752-a8e3-42f1-8307-7b4c35e56cbd_2.png", "wide_ok": True, "kicker": "Voile", "title": "Une essence humide fait plus qu'une crème lourde.", "body": "Le film hydratant donne le rebond. Le gras seul donne juste de la brillance."},
            {"bg": MEDIA/"sonagib_Photoreal_high-end_K-beauty_editorial_close-up_of_a_b_b93dccf7-bce2-49dc-acb9-bed3ed4e54f7_2.png", "wide_ok": True, "kicker": "Outil", "title": "Les devices vendent du futur. La peau veut surtout de la régularité.", "body": "LED, microcourant, massage: intéressants si la routine de base est déjà propre."},
            {"bg": IRIS/"020-beauty-of-joseon-body-v1.webp", "kicker": "À retenir", "title": "Tu peux acheter le résultat sans acheter le mythe.", "body": "SPF, hydratation, barrière. C'est là que la K-beauty garde son avantage."},
            {"bg": MEDIA/"astroboy900802_A_close-up_portrait_of_a_joyful_young_woman_with_612b2453-db6c-4716-89ad-2262627dbb9d.png", "wide_ok": True, "kicker": "À faire", "title": "Cherche le glow qui convient à ta peau.", "body": "Tag boutique à connecter. Quiz routine dans la bio. Article complet sur Sonagi Reference."},
        ],
    },
    {
        "slug": "03-greta-lee-mool-gwang-40",
        "label": "mool-gwang",
        "title": "Greta Lee montre la version adulte de la peau lumineuse",
        "note": "Celebrity routine: Greta Lee. Source: Sonagi Reference celebrity article.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/celebrities/fr/greta-lee/",
        "slides": [
            {"bg": IMG/"celebrities/greta-lee-hero-v3.webp", "wide_ok": True, "kicker": "Peau caméra", "title": "À 40 ans, l'éclat ne vient pas d'une couche brillante.", "body": "Il vient d'une surface calme, hydratée, et d'une routine qu'on ne change pas chaque semaine."},
            {"bg": MEDIA/"beauty of joseon balm.jpg", "wide_ok": True, "kicker": "Soir", "title": "Le baume retire le SPF sans abîmer la barrière.", "body": "C'est le geste discret qui décide si les actifs du lendemain seront tolérés."},
            {"bg": MEDIA/"model_general_european-brunette_studio-Anua Niacinamide serum_v1.png.jpg", "wide_ok": True, "kicker": "Matin", "title": "Le sérum éclat doit travailler lentement.", "body": "Riz, niacinamide, arbutine: pas de coup d'éclat agressif. Une correction patiente."},
            {"bg": IMG/"basics/hormones-age-hero.webp", "kicker": "Âge", "title": "La peau adulte a moins besoin de choc, plus besoin de continuité.", "body": "On ne poursuit pas une peau de 20 ans. On protège la lumière de maintenant.", "visual": DIA/"hormones-et-peau-au-fil-de-l-age-mechanism.webp"},
            {"bg": MEDIA/"sonagib_Editorial_beauty_campaign_close_up_of_a_young_woman_l_6e402c35-5946-4c9c-a1d3-b843852357a5_3.png", "wide_ok": True, "kicker": "Texture", "title": "Mool-gwang veut dire eau-lumière, pas huile.", "body": "Une peau gonflée d'eau reflète mieux. Une peau saturée de gras peut juste étouffer."},
            {"bg": MEDIA/"sonagib_Editorial_K-beauty_close-up_of_a_strikingly_beautiful_7dc40089-1592-4d40-a425-010ac2efa5fb_3.png", "wide_ok": True, "kicker": "Règle", "title": "Plus la peau est sensible, plus la routine doit être ennuyeuse.", "body": "Ennuyeuse n'est pas faible. C'est souvent là que la peau recommence à faire confiance."},
            {"bg": MEDIA/"sonagib_Editorial_K-beauty_close-up_of_a_strikingly_beautiful_7dc40089-1592-4d40-a425-010ac2efa5fb_0.png", "wide_ok": True, "kicker": "À faire", "title": "Construis une routine que tu peux garder six semaines.", "body": "Tag boutique à connecter. Quiz routine dans la bio. Article complet sur Sonagi Reference."},
        ],
    },
    {
        "slug": "04-zendaya-routine-minimaliste",
        "label": "minimalisme",
        "title": "Zendaya a la routine la moins TikTok de Hollywood",
        "note": "Celebrity routine: Zendaya. Source: Sonagi Reference celebrity article.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/celebrities/fr/zendaya/",
        "slides": [
            {"bg": IMG/"celebrities/zendaya-hero-v2.webp", "kicker": "Anti-étagère", "title": "Quatre gestes. Pas une salle de bain entière.", "body": "Nettoyer, tonifier, hydrater, protéger. La routine tient parce qu'elle est simple."},
            {"bg": MEDIA/"u3876414656_Highly_realistic_shot_of_a_young_woman_washing_her__f1004560-e1be-47f5-83c5-49ce8b531091.png", "wide_ok": True, "kicker": "Nettoyage", "title": "Le savon peut nettoyer. Le pH décide s'il respecte.", "body": "La version K-beauty: retirer le SPF sans casser le manteau acide.", "visual": DIA/"le-ph-de-la-peau.webp"},
            {"bg": MEDIA/"assetsimagesingredientsheartleaf-body-1.webp.png", "wide_ok": True, "kicker": "Toner", "title": "Le toner n'est pas une eau parfumée.", "body": "C'est l'étape qui remet la peau en état de recevoir le reste."},
            {"bg": MEDIA/"sonagib_Editorial_beauty_campaign_close-up_Asian_woman_applyi_4704fcba-fadd-4a5b-ac4a-b3efa25b1a63_2.png", "kicker": "Essence", "title": "Une couche humide vaut mieux qu'une crème trop lourde.", "body": "La mucine et les humectants posent le confort sans transformer la peau en film gras."},
            {"bg": IRIS/"024-acne-hormonale-body-v1.webp", "wide_ok": True, "kicker": "Bouton", "title": "Le patch protège mieux que l'attaque réflexe.", "body": "Un bouton qu'on ne touche pas guérit souvent plus proprement."},
            {"bg": IRIS/"019-beauty-of-joseon-hero-v1.webp", "wide_ok": True, "kicker": "SPF", "title": "La seule étape vraiment anti-âge, c'est celle qu'on remet demain.", "body": "SPF tous les jours. Le reste vient après."},
            {"bg": MEDIA/"u3361688922_Smiling_woman_beautiful_confident_nice_teeth_lookin_20ff8a6e-51d3-4a2e-89dc-3fe31016c372.png", "wide_ok": True, "kicker": "À faire", "title": "Si ta routine déborde, enlève avant d'ajouter.", "body": "Tag boutique à connecter. Quiz routine dans la bio. Article complet sur Sonagi Reference."},
        ],
    },
    {
        "slug": "05-sabrina-spf-generation",
        "label": "spf culture",
        "title": "Sabrina Carpenter a compris le produit le moins sexy du glow",
        "note": "Celebrity routine: Sabrina Carpenter. Source: Sonagi Reference celebrity article.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/celebrities/fr/sabrina-carpenter/",
        "slides": [
            {"bg": IMG/"celebrities/sabrina-carpenter-hero-v2.webp", "wide_ok": True, "kicker": "Depuis 15 ans", "title": "Le glow le plus rentable commence par la SPF.", "body": "Pas le sérum rare. Pas le masque viral. La crème solaire, tous les jours."},
            {"bg": MEDIA/"model_general_european-brunette_BoJ_sunscreen_v1.png.jpg", "wide_ok": True, "kicker": "Le vrai luxe", "title": "Une SPF qu'on aime remettre vaut mieux qu'une SPF parfaite qu'on déteste.", "body": "Texture, fini, confort: c'est ce qui décide si tu la portes vraiment."},
            {"bg": IMG/"basics/le-ph-de-la-peau-card-v3.webp", "wide_ok": True, "kicker": "Peau sensible", "title": "La peau sensible veut moins de spectacle.", "body": "Nettoyage doux, pH bas, actifs espacés. La protection vient avant la correction.", "visual": DIA/"le-ph-de-la-peau.webp"},
            {"bg": MEDIA/"model_general_european-brunette_studio-Anua Niacinamide serum_v1.png.jpg", "wide_ok": True, "kicker": "Éclat", "title": "La vitamine C n'est pas obligatoire pour être lumineuse.", "body": "Niacinamide, SPF, hydratation: parfois le glow vient d'une peau moins inflammée."},
            {"bg": MEDIA/"sonagib_Editorial_beauty_campaign_close-up_Asian_woman_applyi_2bec5eb9-18ed-40a3-a1e1-b74e1fea7447_0.png", "kicker": "Calme", "title": "Plus la peau rougit, plus la routine doit parler doucement.", "body": "Un toner apaisant peut être plus utile qu'un actif de plus."},
            {"bg": MEDIA/"Double cleansing hero.png", "wide_ok": True, "kicker": "Soir", "title": "La SPF du matin doit sortir le soir.", "body": "C'est là que le double nettoyage devient logique, pas tendance."},
            {"bg": MEDIA/"danielzoldi_close-up_portrait_of_smiling_woman_with_radiant_ski_2653f84b-cbc1-455b-bb96-870ebfc9dcc6.png", "wide_ok": True, "kicker": "À faire", "title": "Commence par la SPF que tu porteras vraiment.", "body": "Tag boutique à connecter. Quiz routine dans la bio. Article complet sur Sonagi Reference."},
        ],
    },
    {
        "slug": "06-selena-barriere-peau-sensible",
        "label": "peau sensible",
        "title": "La vraie routine de star, c'est celle qui n'enflamme pas la peau",
        "note": "Celebrity routine angle: sensitive skin / barrier logic using Sonagi Reference celebrity assets.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/celebrities/fr/selena-gomez/",
        "slides": [
            {"bg": IMG/"celebrities/selena-gomez-hero-v2.webp", "wide_ok": True, "kicker": "Red carpet", "title": "Une peau maquillée souvent doit surtout récupérer souvent.", "body": "La question n'est pas seulement le produit posé. C'est ce que la peau tolère après."},
            {"bg": MEDIA/"sonagib_Editorial_beauty_campaign_close-up_of_a_young_woman_i_43deef67-139b-4771-a912-99e707fe1581_2.png", "kicker": "Barrière", "title": "Si tout pique, la routine parle trop fort.", "body": "La barrière abîmée transforme même de bons actifs en problème.", "visual": DIA/"la-barriere-cutanee.webp"},
            {"bg": MEDIA/"Centella Asiatica hero.png", "wide_ok": True, "kicker": "Calme", "title": "Centella, heartleaf, beta-glucane: les ingrédients sans ego.", "body": "Ils ne promettent pas une nouvelle peau. Ils aident la peau à redevenir tolérante."},
            {"bg": MEDIA/"sonagib_Editorial_beauty_campaign_close_up_of_a_young_woman_l_6e402c35-5946-4c9c-a1d3-b843852357a5_1.png", "wide_ok": True, "kicker": "Hydratation", "title": "Une peau sensible manque souvent d'eau avant de manquer d'actifs.", "body": "Remettre de l'eau peut calmer plus vite que corriger."},
            {"bg": IRIS/"024-acne-hormonale-body-v1.webp", "wide_ok": True, "kicker": "Boutons", "title": "Protéger un bouton peut être plus intelligent que l'assécher.", "body": "Le patch limite le grattage, donc limite aussi la marque."},
            {"bg": IRIS/"019-beauty-of-joseon-hero-v1.webp", "wide_ok": True, "kicker": "SPF", "title": "La peau sensible a besoin de protection, pas d'excuse.", "body": "Cherche une texture que tu peux porter sans brûler les yeux ni rougir."},
            {"bg": MEDIA/"murketingzoopt_A_blonde_woman_lying_on_her_stomach_with_a_tall__07b865b6-9c5a-488d-a3f0-6bdb613cc22f.png", "wide_ok": True, "kicker": "À faire", "title": "Ta routine doit calmer avant de performer.", "body": "Tag boutique à connecter. Quiz routine dans la bio. Article complet sur Sonagi Reference."},
        ],
    },
    {
        "slug": "07-sephora-kids-age-anxiete",
        "label": "société",
        "title": "Sephora Kids: le vrai sujet, ce n'est pas la peau. C'est l'angoisse.",
        "note": "Societal trend: Gen Alpha, anti-aging anxiety, routine boundaries.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/edito/fr/sephora-kids/",
        "slides": [
            {"bg": MEDIA/"u8241935354_A_stylish_Gen_Z_Korean_girl_surrounded_by_pastel-co_eb4bf7cb-5a2b-4a27-9b44-acf6ecdb4c8f.png", "wide_ok": True, "kicker": "Trend toxique", "title": "Quand une enfant demande du rétinol, ce n'est pas une question de peau.", "body": "C'est une question d'algorithme, de peur, et d'adultes qui ont vendu l'anti-âge trop tôt."},
            {"bg": MEDIA/"children routine.png", "wide_ok": True, "kicker": "Besoin réel", "title": "Avant la puberté, la peau demande surtout trois choses.", "body": "Nettoyage doux, hydratation simple, SPF. Pas une routine d'adulte miniaturisée.", "visual": DIA/"routine-enfant-mechanism.webp"},
            {"bg": MEDIA/"beauty of joseon spf cream.jpg", "wide_ok": True, "kicker": "Le bon luxe", "title": "La SPF est une éducation, pas une obsession.", "body": "On apprend la protection sans transformer le visage en projet à corriger."},
            {"bg": MEDIA/"daughter Kbeauty case.jpeg", "wide_ok": True, "kicker": "Le risque", "title": "Les actifs trop tôt peuvent abîmer la confiance autant que la barrière.", "body": "Quand ça pique, rougit, pèle: l'enfant apprend que sa peau est un problème."},
            {"bg": MEDIA/"EDITORIAL HERO — routine-enfant.png", "wide_ok": True, "kicker": "Culture", "title": "La beauté adulte a glissé dans les cartables.", "body": "Ce n'est pas aux enfants de résister seules au marketing."},
            {"bg": IMG/"routines/routine-pre-ado-hero.webp", "wide_ok": True, "kicker": "Solution", "title": "Une routine courte peut être un geste de protection.", "body": "Pas parce que le soin est mauvais. Parce que l'enfance mérite de rester légère."},
            {"bg": MEDIA/"malangzo_a_super_cute_18-year-old_Korean_girl_seems_like_a_k-po_f9893208-fecc-4693-8451-8a6c7f6696e6.png", "wide_ok": True, "kicker": "À faire", "title": "Pour une jeune peau: routine minimale, adulte responsable.", "body": "Tag boutique à connecter. Quiz routine dans la bio. Article complet sur Sonagi Reference."},
        ],
    },
    {
        "slug": "08-ozempic-face-kbeauty",
        "label": "visage 2026",
        "title": "Ozempic face a déplacé l'anti-âge vers le volume",
        "note": "Societal trend: GLP-1, facial volume loss, K-beauty support.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/edito/fr/ozempic-face-kbeauty/",
        "slides": [
            {"bg": MEDIA/"Ozempic hero.jpeg", "wide_ok": True, "kicker": "Nouveau visage", "title": "Le débat beauté de 2026 n'est pas seulement la ride. C'est le volume.", "body": "Perte de poids rapide, visage creusé, peau qui semble plus fine: la routine doit changer de vocabulaire."},
            {"bg": MEDIA/"ozempic model how to use pen.jpg", "wide_ok": True, "kicker": "Mécanisme", "title": "Quand le soutien baisse, la peau ne peut pas tout porter seule.", "body": "Le soin cosmétique ne remplace pas le volume. Il peut soutenir barrière, eau, éclat.", "visual": IMG/"edito/ozempic-face-kbeauty/ozempic-face-volume-loss-progression.webp"},
            {"bg": MEDIA/"PDRN amazing.png", "wide_ok": True, "kicker": "Actif", "title": "PDRN, peptides, cica: la nouvelle grammaire réparation.", "body": "La K-beauty vend moins le choc, plus le support."},
            {"bg": MEDIA/"sonagib_Editorial_beauty_campaign_close_up_of_a_young_woman_l_6e402c35-5946-4c9c-a1d3-b843852357a5_2.png", "wide_ok": True, "kicker": "Hydratation", "title": "Une peau déshydratée paraît plus creusée.", "body": "Remettre de l'eau ne recrée pas le volume, mais ça adoucit la lecture du visage."},
            {"bg": IMG/"techniques/skin-flooding-body-1.webp", "kicker": "Stack", "title": "Le stack utile: SPF, hydratation, barrière, patience.", "body": "Pas dix actifs agressifs sur une peau déjà en transition.", "visual": DIA/"pdrn-mechanism.webp"},
            {"bg": MEDIA/"over 60 basics.png", "wide_ok": True, "kicker": "Honnêteté", "title": "Le cosmétique accompagne. Il ne remplace pas la médecine.", "body": "Son rôle: rendre la peau plus confortable, plus lumineuse, moins vulnérable."},
            {"bg": MEDIA/"sonagib_Editorial_K-beauty_close-up_of_a_strikingly_beautiful_c4082e5d-f1ae-471d-841c-5e891e2f16f4_3.png", "wide_ok": True, "kicker": "À faire", "title": "Construis une routine de soutien, pas de panique.", "body": "Tag boutique à connecter. Quiz routine dans la bio. Article complet sur Sonagi Reference."},
        ],
    },
    {
        "slug": "09-pdrn-salmon-dna-societe",
        "label": "actif viral",
        "title": "PDRN: pourquoi tout le monde veut de l'ADN de saumon",
        "note": "Trend: PDRN / salmon DNA / repair culture.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/ingredients/fr/pdrn/",
        "slides": [
            {"bg": MEDIA/"PDRN amazing.png", "wide_ok": True, "kicker": "Actif 2026", "title": "Le nouveau fantasme beauté, ce n'est plus décaper. C'est réparer.", "body": "PDRN, exosomes, peptides: le langage a changé. On veut une peau qui récupère."},
            {"bg": MEDIA/"PDRN.png", "wide_ok": True, "kicker": "Le mot", "title": "PDRN signifie polydésoxyribonucléotide.", "body": "Oui, c'est moins vendable qu'un joli nom. Mais l'idée est simple: signal de réparation.", "visual": DIA/"pdrn-mechanism.webp"},
            {"bg": MEDIA/"sonagib_Editorial_beauty_campaign_close-up_of_a_young_woman_i_57e49514-f324-42dd-9c61-9ee0d83ec6db_1.png", "kicker": "Culture", "title": "La peau fatiguée est devenue un sujet social.", "body": "Manque de sommeil, stress, actifs trop forts: la réparation devient le nouveau luxe."},
            {"bg": MEDIA/"sonagib_Editorial_beauty_still_photograph_Vogue_Korea_hall-of_b5fe50bd-839e-4ec1-a202-81abb0b28064_0.png", "wide_ok": True, "kicker": "Clinique", "title": "En Corée, le soin clinique inspire le retail.", "body": "Les tendances sortent souvent des cabinets, puis deviennent sérums, ampoules, masques."},
            {"bg": MEDIA/"centella asiatica.png", "wide_ok": True, "kicker": "À ne pas confondre", "title": "Un sérum PDRN n'est pas une injection.", "body": "Même mot, intensité différente. Il faut garder les promesses à leur taille."},
            {"bg": MEDIA/"sonagib_Editorial_beauty_campaign_close-up_of_a_young_woman_i_43deef67-139b-4771-a912-99e707fe1581_0.png", "kicker": "Routine", "title": "Si ta barrière est cassée, commence plus bas.", "body": "Nettoyant doux, crème, SPF. Les actifs réparation viennent quand la peau tolère."},
            {"bg": MEDIA/"sonagib_Editorial_K-beauty_close-up_portrait_of_a_confident_F_d83a544a-befb-4384-be15-0d4f17b02322_3.png", "wide_ok": True, "kicker": "À faire", "title": "Répare avant de chercher plus fort.", "body": "Tag boutique à connecter. Quiz routine dans la bio. Article complet sur Sonagi Reference."},
        ],
    },
    {
        "slug": "10-underconsumption-skincare",
        "label": "anti-haul",
        "title": "La tendance la plus chic en skincare: acheter moins",
        "note": "Societal trend: underconsumption, deinfluencing, skinimalism.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/routines/fr/routine-asma/",
        "slides": [
            {"bg": MEDIA/"Asma hero.png", "wide_ok": True, "kicker": "Anti-haul", "title": "Ta peau ne veut pas une nouveauté par semaine.", "body": "Elle veut comprendre ce qui arrive, et le recevoir assez longtemps pour répondre."},
            {"bg": IMG/"basics/ppm-hero.webp", "kicker": "Trop", "title": "Plus de produits ne veut pas dire plus de résultats.", "body": "Parfois, ça veut juste dire plus d'irritation, plus de confusion, plus de déchets."},
            {"bg": IMG/"basics/la-barriere-cutanee-body-1.webp", "kicker": "Barrière", "title": "Une barrière stressée ne distingue plus le bon du mauvais.", "body": "Quand tout pique, le problème n'est pas toujours le produit. C'est l'empilement.", "visual": DIA/"la-barriere-cutanee.webp"},
            {"bg": MEDIA/"model_general_european-brunette_studio-portrait_cream_v1.png.jpg", "wide_ok": True, "kicker": "Garde", "title": "Garde ce qui calme, ce qui protège, ce que tu finis.", "body": "Un produit racheté trois fois vaut mieux que dix produits presque pleins."},
            {"bg": MEDIA/"model_general_european-brunette_bathroom-routine_cream_v3.png.jpg", "wide_ok": True, "kicker": "Règle", "title": "Nettoyant, hydratant, SPF. Ensuite seulement, un actif.", "body": "La routine courte n'est pas pauvre. Elle est lisible."},
            {"bg": MEDIA/"model_general_european-brunette_cafe-lifestyle_cream_v1.png.jpg", "wide_ok": True, "kicker": "Luxe", "title": "Le vrai luxe, c'est une peau stable.", "body": "Pas une salle de bain qui ressemble à un magasin."},
            {"bg": MEDIA/"model_general_european-brunette_studio-portrait_pink_v1.png.png", "wide_ok": True, "kicker": "À faire", "title": "Fais l'inventaire avant d'acheter.", "body": "Tag boutique à connecter. Quiz routine dans la bio. Article complet sur Sonagi Reference."},
        ],
    },
    {
        "slug": "11-spf-is-the-new-serum",
        "label": "spf quotidien",
        "title": "La SPF est devenue le nouveau sérum",
        "note": "Trend: SPF as daily skincare, not beach product.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/brands/fr/beauty-of-joseon/",
        "slides": [
            {"bg": IRIS/"019-beauty-of-joseon-hero-v1.webp", "wide_ok": True, "kicker": "Hot take", "title": "Si tu dois choisir un seul anti-âge, prends la SPF.", "body": "Pas parce qu'elle est glamour. Parce qu'elle travaille tous les jours."},
            {"bg": MEDIA/"model_general_european-brunette_BoJ_sunscreen_v1.png.jpg", "wide_ok": True, "kicker": "Fini", "title": "La K-beauty a gagné parce qu'elle a rendu la SPF agréable.", "body": "Une texture que tu as envie de porter change plus que la promesse sur le tube."},
            {"bg": IMG/"basics/hormones-age-hero.webp", "kicker": "Long terme", "title": "Taches, texture, perte d'éclat: le soleil signe partout.", "body": "La meilleure correction est souvent celle qu'on évite de devoir faire.", "visual": DIA/"skin-aging-mechanism.webp"},
            {"bg": MEDIA/"children routine.png", "wide_ok": True, "kicker": "Éducation", "title": "Apprendre la SPF tôt n'est pas apprendre la peur.", "body": "C'est apprendre que la peau mérite une protection normale, comme les dents."},
            {"bg": MEDIA/"beauty of joseon spf cream.jpg", "wide_ok": True, "kicker": "Shopping", "title": "Le bon SPF ne se juge pas seulement à l'indice.", "body": "Il se juge au fini, aux yeux, à la compatibilité maquillage, et à l'envie de le remettre."},
            {"bg": MEDIA/"Double Cleansing body.png", "wide_ok": True, "kicker": "Soir", "title": "La SPF est un engagement matin et soir.", "body": "Tu la mets le matin. Tu la retires correctement le soir."},
            {"bg": MEDIA/"mjhw6694_A_radiant_Korean_beauty_campaign_image_of_a_young_woma_b52b186a-98cd-47ee-a514-29f21e43e600.png", "wide_ok": True, "kicker": "À faire", "title": "Trouve une SPF que tu ne négocies pas.", "body": "Tag boutique à connecter. Quiz routine dans la bio. Article complet sur Sonagi Reference."},
        ],
    },
    {
        "slug": "12-kbeauty-clinique-retail",
        "label": "séoul effect",
        "title": "La K-beauty 2026 ressemble de plus en plus à une clinique douce",
        "note": "Trend: clinic-to-retail actives, repair, devices, realistic claims.",
        "quiz_url": "sonagibeauty.com/consultation.html",
        "article_url": "sonagibeauty.com/ref/techniques/fr/rejuran/",
        "slides": [
            {"bg": MEDIA/"sonagib_Editorial_beauty_still_photograph_Vogue_Korea_hall-of_9d7d8b86-5718-4414-b609-e18d25a1bc20_2.png", "wide_ok": True, "kicker": "Séoul effect", "title": "Les tendances ne viennent plus seulement des rayons. Elles viennent des cliniques.", "body": "PDRN, Rejuran, LED, boosters: le vocabulaire soin devient plus technique."},
            {"bg": MEDIA/"PDRN.png", "wide_ok": True, "kicker": "Retail", "title": "Mais un sérum n'est pas une procédure.", "body": "Même inspiration, autre intensité. C'est là qu'une marque sérieuse doit rester honnête.", "visual": DIA/"rejuran-mechanism.webp"},
            {"bg": MEDIA/"PDRN amazing.png", "wide_ok": True, "kicker": "Device", "title": "Les outils marchent mieux sur une routine stable.", "body": "Un device ne sauve pas une barrière maltraitée."},
            {"bg": MEDIA/"sonagib_Editorial_beauty_campaign_close-up_of_a_young_woman_i_57e49514-f324-42dd-9c61-9ee0d83ec6db_3.png", "kicker": "Réparation", "title": "Le mot-clé n'est plus transformer. C'est récupérer.", "body": "La peau moderne est fatiguée. La K-beauty répond avec support, pas punition."},
            {"bg": MEDIA/"Centella Asiatica hero.png", "wide_ok": True, "kicker": "Actifs doux", "title": "Beta-glucane, centella, cica: le calme devient premium.", "body": "La douceur n'est plus l'option débutante. C'est la stratégie longue."},
            {"bg": IMG/"basics/ppm-hero.webp", "kicker": "Dosage", "title": "La sophistication, c'est savoir doser.", "body": "Pas tout, pas tout de suite, pas tous les soirs."},
            {"bg": MEDIA/"sonagib_Editorial_beauty_campaign_close-up_Asian_woman_applyi_4704fcba-fadd-4a5b-ac4a-b3efa25b1a63_1.png", "wide_ok": True, "kicker": "À faire", "title": "Demande toujours: retail ou procédure?", "body": "Tag boutique à connecter. Quiz routine dans la bio. Article complet sur Sonagi Reference."},
        ],
    },
]

if __name__ == "__main__":
    bank.main()
