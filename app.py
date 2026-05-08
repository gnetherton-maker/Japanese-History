import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

#PAGE SETUP
st.set_page_config(page_title="Unification Tactics Dashboard", layout="wide")

st.title("The Mechanics of Unification")
st.markdown("### Military Dominance and expansion of the three great rulers, Nobunaga, Hideyoshi, and Ieyasu (1560–1615)")

# EXPANSION EVENTS, on the map
map_data = {
    'Year': [1560, 1570, 1575, 1582, 1584, 1585, 1587, 1590, 1592, 1600, 1603, 1615],
    'Event': [
        'Battle of Okehazama', 
        'Siege of Kanegasaki', 
        'Battle of Nagashino', 
        'Honnō-ji Incident', 
        'Battle of Komaki and Nagakute', 
        'Shikoku Campaign', 
        'Kyushu Campaign', 
        'Siege of Odawara', 
        'Invasions of Korea (Imjin War)', 
        'Battle of Sekigahara', 
        'Edo Castle (Sankin-kōtai Center)', 
        'Siege of Osaka'
    ],
    'Leader': ['Nobunaga', 'Nobunaga', 'Nobunaga', 'Nobunaga', 'Ieyasu', 'Hideyoshi', 'Hideyoshi', 'Hideyoshi', 'Hideyoshi', 'Ieyasu', 'Ieyasu', 'Ieyasu'],
    'Lat': [35.05, 35.68, 34.92, 35.01, 35.29, 33.76, 32.79, 35.24, 35.10, 35.36, 35.68, 34.68],
    'Lon': [136.95, 136.03, 137.55, 135.75, 136.93, 133.53, 130.74, 139.15, 129.03, 136.46, 139.75, 135.52],
    'Source': [
        "Shinchō Kōki", 
        "Shinchō Kōki", 
        "Shinchō Kōki", 
        "Death Records", 
        "Mikawa Monogatari", 
        "Hideyoshi's Letters", 
        "Hideyoshi's Letters", 
        "Hideyoshi's Letters", 
        "Japanese and Korean Chronicles", 
        "Ieyasu's Letters", 
        "Tokugawa Edicts", 
        "Edicts"
    ]
}
df_map = pd.DataFrame(map_data)

# INNOVATIONS
innovation_data = {
    'Year': [1543, 1576, 1578, 1588, 1592, 1603],
    'Innovation': ['Tanegashima (Firearms)', 'Azuchi Stone Walls', 'Ironclad Atakebune', 'The Sword Hunt', 'Wajō (Korean Castles)', 'Sankin-kōtai (Hostage System)'],
    'Category': ['Weapons', 'Fortification', 'Naval Warfare', 'Disarmament', 'Base Building', 'Controlling Diplomacy'],
    'Impact': ['Revolutionized infantry combat.', 'Heavy fortification vs cannons.', 'Armored ships to break blockades and dominate waterways.', 'Disarmed the population, weakening Daimyō.', 'Secured overseas supply lines.', 'Ensured vassal compliance.']
}
df_innov = pd.DataFrame(innovation_data)

# THE SLIDER 
selected_year = st.select_slider("Adjust Timeline to View Expansion Process", options=range(1540, 1620, 5))

#FILTERING
current_map_df = df_map[df_map['Year'] <= selected_year]
current_innov_df = df_innov[df_innov['Year'] <= selected_year]

#MAP
st.subheader(f"Territorial Expansion & Tactics as of {selected_year}")
fig_map = px.scatter_mapbox(
    current_map_df,
    lat="Lat", lon="Lon",
    hover_name="Event",
    color="Leader",
    hover_data={"Lat": False, "Lon": False},
    zoom=5.1,
    height=500,
    color_discrete_map={"Nobunaga": "red", "Hideyoshi": "blue", "Ieyasu": "green"}
)

# --- DYNAMIC TERRITORY GLOW LOGIC ---
glow_lat = []
glow_lon = []
glow_color = ""
glow_radius = 0

if 1560 <= selected_year < 1582:
    # Nobunaga (Red): Glowing heavily around greater Kyoto/Central Japan, 
    # plus West (Chugoku border) and Northeast (Kaga/Echizen)
    glow_lat = [35.0, 35.3, 34.8, 34.8, 36.5] 
    glow_lon = [135.7, 136.5, 136.0, 134.5, 136.6]
    glow_color = "red"
    glow_radius = 85 # Expanded radius for heavier glow
    
elif 1582 <= selected_year < 1600:
    # Hideyoshi (Blue): Honshu, Kyushu, Shikoku
    glow_lat = [36.2, 34.7, 39.0, 33.0, 33.7]
    glow_lon = [138.0, 135.5, 140.5, 131.0, 133.5]
    
    # Korea glows blue during the Imjin War (1590-1595 sliders)
    if selected_year >= 1590: 
        glow_lat.extend([37.5, 36.0, 39.0])
        glow_lon.extend([127.0, 128.0, 126.0])
        
    glow_color = "blue"
    glow_radius = 100
    
elif selected_year >= 1600:
    # Ieyasu (Green): Honshu, Kyushu, Shikoku
    glow_lat = [36.2, 34.7, 39.0, 33.0, 33.7]
    glow_lon = [138.0, 135.5, 140.5, 131.0, 133.5]
    glow_color = "green"
    glow_radius = 100

# Apply the glow to the map if data exists for the selected year
if glow_lat:
    color_rgba = {
        "red": "rgba(255, 0, 0, 0.45)", 
        "blue": "rgba(0, 100, 255, 0.4)", 
        "green": "rgba(0, 200, 0, 0.4)"
    }
    fig_map.add_trace(go.Densitymapbox(
        lat=glow_lat,
        lon=glow_lon,
        z=[1] * len(glow_lat),
        radius=glow_radius,
        colorscale=[[0, 'rgba(0,0,0,0)'], [1, color_rgba[glow_color]]],
        showscale=False,
        hoverinfo='skip' # Prevents weird popups on the glow itself
    ))

fig_map.update_layout(mapbox_style="carto-positron")
st.plotly_chart(fig_map, use_container_width=True)

# INNOVATION TIMELINE
st.write("---")
st.subheader("Tactical & Structural Innovations")

if not current_innov_df.empty:
    fig_timeline = px.scatter(
        current_innov_df, 
        x="Year", 
        y=[1] * len(current_innov_df), 
        text="Innovation",
        color="Category",
        hover_data=["Impact"],
        height=300
    )
    
    fig_timeline.update_traces(textposition='top center', marker=dict(size=15))
    fig_timeline.update_yaxes(visible=False, showgrid=False)
    fig_timeline.update_xaxes(range=[1540, 1620], showgrid=True)
    fig_timeline.update_layout(showlegend=True, margin=dict(l=20, r=20, t=20, b=20))
    
    st.plotly_chart(fig_timeline, use_container_width=True)
else:
    st.info("Move the slider past 1540 to begin.")

# --- BIBLIOGRAPHY / SOURCES SECTION ---
st.write("---") 

with st.expander("📚 Project Bibliography & Source Citations"):
    st.markdown("""
    * [1] Lidin, Olof G. *Tanegashima: The Arrival of Europe in Japan*. Copenhagen: NIAS Press, 2002.
    * [2] Totman, Conrad. *Early Modern Japan*. Berkeley: University of California Press, 1993.
    * [3] Ōta, Gyūichi. *The Chronicle of Lord Nobunaga*. Translated and edited by J. S. A. Elisonas and Jeroen Pieter Lamers. Leiden: Brill, 2011.
    * [4]Toyotomi, Hideyoshi. "Restriction on the Use of Weapons, 1588 (The 'Sword Hunt')." Asia for Educators, Columbia University. Accessed May 7, 2026. https://afe.easia.columbia.edu/ps/japan/tokugawa_edicts_swords.pdf.
    * [5] Unknown Artist. *Battle of Pyongyang* (Detail from a folding screen depicting the Imjin War). Late 16th/Early 17th Century. 
    * [6] Nippon.com. "The Battle of Sekigahara: A Turning Point in Japanese History." Nippon.com. Accessed May 7, 2026. https://www.nippon.com/en/japan-topics/b06916/. 
    * [7] Anonymous Engraver. "Bestorming van 't slot Osacca" (Siege of Osaka Castle). In *Gedenkwaerdige Gesantschappen der Oost-Indische Maatschappy in 't Vereenigde Nederland aan de Kaisaren van Japan*, by Arnoldus Montanus. Amsterdam: Jacob Meurs, 1669.
    """)

#SIDEBAR ANALYSIS SECTION
st.sidebar.header("Tactical & Source Analysis")

if selected_year < 1560:
    st.sidebar.subheader("Pre-Unification")
    st.sidebar.write("""
    **Phase:** Warring States and the introduction of firearms.
    
    During this time, Japan consisted of multiple powerful Daimyō who controlled their 
    respective domains. There was no one person who held a significant amount of authority
    over the majority of the country. In 1543, the introduction of the Tanegashima (matchlock) 
    to Japan from Portuguese sailors completely changed warfare on the islands. The samurai
    of Japan who had been using katanas had to change the way they fought to adapt to this 
    new innovation.  Although
    the Japanese copies of the matchlock were "not perfect, Tokitaka (a Daimyō is southern Japan)was immediatly prepared
    to use it," leading to a "decisive outcome [for the] battle" [1]. Guns were arguably the most 
    important innovation in Japanese warfare, and played a critical role in the eventual unification 
    of Japan
    """)

elif 1560 <= selected_year < 1582:
    st.sidebar.subheader("The Era of Nobunaga")
    st.sidebar.write(f"**Current Focus:** Total War & Innovation")
    st.sidebar.write(f"**Latest Event on Map:** {current_map_df.iloc[-1]['Event'] if not current_map_df.empty else 'N/A'}")
    
    st.sidebar.markdown("""
    Oda Nobunaga started out as a Daimyō located in the Nobi plain. one of his first major
    victories occurred in the spring of 1560 against Imagawa Yoshimoto in the battle of Okehazama. Yoshimoto commanded an 
    army of roughly 25,000 compared to Nobunaga's 2,000 (lower estimates used for both parties), 
    and intended to squash out the smaller force. descriptions of how a 
    "heavy downpour" caused Yoshimoto to set up a camp for his troops, but despite the downpour Nobunaga 
    ordered a "suprise assault" resulting in his decisive victory [2]. The young Nobunaga demonstrated elite 
    military tactics that reflected the violence of Sengoku period. The battle of Okehazama established Nobunaga as one of 
    the most dominant Daimyō in the region, and his tactics continued to contributed to his future success.
   
    Nobunaga's expansion was a showing of his military prowess and was often associated with a certain level of brutality.
    Nobunaga's assault on Mount Hiei in 1571 is a prime example. The Mount Hiei monastery was an influential and powerful institution
    of Tendai Buddhism. Nobunaga led an army to Mount Hiei, burned the Enryakuji temple, and had a "multitude of priests as well as lay
    folk put to death [3]. To understand Nobunaga's assault in a military context, you need to understand 
    Mount Hiei's power. Not only did it have signficant religious influence over a vast portion of Japan, but it had its own army dedicated
    serving the religious leaders. Nobunaga's assault on the monastery eliminated this powerful institution and the way he carried it out sent a 
    message to others. The brutality towards priests and other non warriors demonstrated Nobunaga's use of extreme force to punish others
    which he used to divert other groups from opposing him. His display of force led Totman to describe Nobunaga's "claim to 
    primacy on the evidence that his armies could pound rivals into submission" [2]. His diplay of force was a trademark of his expansion.

    One well known integration of the previously mentioned innovation of matchlocks was the Battle of Nagashino in 1575. Nobunaga and future shogun
    Ieyasu fought the Takeda clan who were notable for their use of cavalry. Nobunaga's forces utilizes thousands of matchlocks while holding a defensive
    position to counter the cavalry. This battle is often considered to be one of if not the first "modern" battle in Japan due to the substantial use of
    firearms. Nobunaga contstantly evolded his style of fighting to adapt enemy forces, allowing him to take an un-unified japan and lay the foundation 
    for the eventual unification of the country.
        
    In additio to matchlocks Nobunaga constantly employed new advances in military technology to maintain his dominance. His use of Atakebune (ironclad warships) to control the inland sea
    and stone walls to fortify castles allwoed him to dominate all battlefields, controlling central Honshu with an iron grip.
    """)

elif 1582 <= selected_year < 1598:
    st.sidebar.subheader("The Era of Hideyoshi")
    st.sidebar.write("**Current Focus:** quick expansion and establishing control")
    
    st.sidebar.markdown("""
    After the death of Nobunaga in 1582, one of his generals, Hideyoshi, continued the process of unification. Using the foundation laid out by Nobunaga, Hideyoshi
    expanded the territoy under his control to the northern regeions of Honshu and the southern islands of Shikoku and Kushū.

    Like Nobunaga, Hideoyshi also employed brutal tactics on his opponents when necessary. However, he also utilized diplomatic means to weaken his rivals and expand his power. After taking control,
    Hideyoshi startgegically utilized diplomacy and regulations to cripple those that could oppose him and force the into submission.
    Hideyoshi's policies directly restricted the possibility of revolt, acting as a form of militaristic control. Hideyoshi's "sword hunt" was a prime example of control.
    This policy aimed to disarm all peoples by demanding the surrender of their weapons, significantly lowering the chances of revolt and the strength of other regional lords. 
    An english translation of the edict goes as follows "Farmers of all provinces are strictly forbidden to have in their possession any swords,
    shortswords, bows, spears, firearms, or other types of weapons" [4]. The sword hunt was very clearly a way to limit the power  of the population and other Daimyō. An interesting thing to note is the way
    which this policy was justified. the metal scraps were said the be "used in the construction of the great image of Buddha," resulting in a better afterlife for those who donated [4]. The framingof this policy in a religious context
    shows Hideyoshis understanding of Japan's culture. Doing this allows his edict to seem more justifiable to the common person, further decreasing the chances of rresentment or revolt.
    This forced policy was one of many non violent tactics Hideyoshi used to maintain his control, and increase his respective military dominance.


    The Imjin Wars were a strong examples of Hideyoshi's military conquest, and the ambitions he had for Japans expansion. Hideyoshi's plan involved invading and conquering Korea, then using 
    Korean soliders for the front line of an assault on Ming China. Hideyoshi successfully captured all of modern day South Korea, reaching the capitol of HanSeong, and continued advancing foward
    advancing further north into modern day North Korea, reaching Pyongyang.
    """)
    
    # IMAGE INSERTION - PYONGYANG
    if os.path.exists("Pyongyang.jpg"):
        st.sidebar.image("Pyongyang.jpg", caption="The Battle of Pyongyang [5]", use_container_width=True)
    else:
        st.sidebar.warning("Pyongyang.jpg not found. Please ensure the image is in the same folder as app.py.")

    st.sidebar.markdown("""
    The battle of Pyongyang depicted in the painting above, was one of the many battles in the Imjin Wars. The Japanese having already captured Pyongyang continued to hold on to the city following joint Ming and Korean attempts to reclaim it. 
    This image depicts one of the many large scale battles that Hideyoshi had to fight to extend the reach of his domain
    Similar to Nobunaga's conquests, Hideyoshi also employed brutal tactics during his advances into the Korean Peninsula. A reward system based on collecting the noses of Korean enemies 
    encouraged the slaughtering of not only Korean soliders, but also civilians. Another commenly employed tactic was the kidnapping of Korean civilians to be used as slaves in mainland Japan. Due to the shortage of Labor 
    because of the War, kidnapped Koreans were forced into labor and servitude, enduring cruel conditions.
    """)

else: # 1598 to 1615
    st.sidebar.subheader("The Era of Ieyasu")
    st.sidebar.write("**Current Focus:** Forcing Stability")
    
    st.sidebar.markdown("""
    Ieyasu Tokugawa, the final of the three great unifiers also had to stand out in battle, but a lot of his military genius was a result of calculated diplomacy and alliance building. At the death of Hideyoshi, Japan 
    had become significantly more unified compared than when Nobunaga came into power. As a result, absolute brutality was not what Ieyasu needed to achieve to consolodate power, rather, forming a lasting empire required much more 
    strategic diplomacy.

    Despite the a shift in necessary tactics, Ieyasu still required military dominance and displays of force to achieve total control over Japan. Notably, the beginning of his claim to power, and the final defeat of opposing challengers were marked in large scale battles.
    Leading up to the battle of Sekigahara in 1600, Ieyasu built strong alliances with powerful Daimyō, making them "pledge loyalty" [6] to him. Forming these alliances were crucial to defeating the Western army, which was 
    another coalition of Daimyō and the successors of Toyotomi Hideyoshi. This battle is often considered the largest in Japanese history, with approximately 160,000 warriors partaking. To win a battle at this scale requires a keen
    military understanding, which Iyesau proved to have. Additionally, Ieyasu's final conflict resolution to power came with the siege of Osaka, where the former shogunate family, the Toyotomi clan, was eradicated. 
    """)

    # IMAGE INSERTION - OSAKA
    if os.path.exists("Osaka.png"):
        st.sidebar.image("Osaka.png", caption="The Siege of Osaka (1615) [7]", use_container_width=True)
    else:
        st.sidebar.warning("Osaka.png not found. Please ensure the image is in the same folder as app.py.")

    st.sidebar.markdown("""
    Tokugawa forces lead an assault of the fortress, burning it to the ground as seen in the woodblock printing of the battle. The burning of the Toyotomi's last stronghold was symbolic of the change in power, 
    cementing Tokugawa rule. This last show of power officailly started the era of consolidated power. 

    After decades of blood filled battles, Ieyasu's alternate attendance system (hostage system) was the critical policy 
    that forced other Daimyō into weakened positions while maintaining shogunate control. By holding Daimyō's family hostage in the capital, Ieyasu
    would have leverage in any military conflict. This policy allowed the Tokugawa to maintain control for over 250 years.
    """)