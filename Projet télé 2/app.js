const map = L.map('map', {
    crs: L.CRS.Simple,
    minZoom: -1
  });
  
  const imageWidth = 1000;
  const imageHeight = 700;
  const bounds = [[0, 0], [imageHeight, imageWidth]];
  const image = L.imageOverlay('images/PlanCESI-RDC.png', bounds).addTo(map);
  map.fitBounds(bounds);
  
  // Légende
  const legend = L.control({ position: "bottomright" });
  legend.onAdd = function () {
    const div = L.DomUtil.create("div", "legend");
    div.innerHTML = `
      <b>Légende :</b><br>
      <span style="color:green">●</span> Fonctionnelle<br>
      <span style="color:red">●</span> En panne<br>
      <span style="color:blue">●</span> Réservée
    `;
    return div;
  };
  legend.addTo(map);
  
  // Chargement des télés
  const markersMap = new Map(); // Clé = nom de télé, valeur = marker

fetch("data/teles.json")
  .then(res => res.json())
  .then(teles => {
    teles.forEach(tele => {
      let color = {
        "Fonctionnelle": "green",
        "En panne": "red",
        "Réservée": "blue"
      }[tele.etat] || "gray";

      const marker = L.circleMarker([tele.y, tele.x], {
        radius: 10,
        fillColor: color,
        color: "#000",
        weight: 1,
        opacity: 1,
        fillOpacity: 0.8
      }).addTo(map);

      const content = generatePopupContent(tele);
      marker.bindPopup(content);

      markersMap.set(tele.nom, { marker, tele });
    });
  });

function reserverTele(nom) {
  const item = markersMap.get(nom);
  if (!item) return;

  item.tele.etat = "Réservée"; // mise à jour de l'état
  item.marker.setStyle({ fillColor: "blue" }); // mise à jour de la couleur

  // mise à jour du popup
  const newPopup = generatePopupContent(item.tele);
  item.marker.setPopupContent(newPopup);

  alert(`✅ Réservation confirmée pour la télé : ${nom}`);
}

function generatePopupContent(tele) {
  let actionButton = "";
  if (tele.etat === "Réservée") {
    actionButton = `<button class="popup-btn" onclick="annulerReservation('${tele.nom}')">Annuler</button>`;
  } else if (tele.reservable) {
    actionButton = `<button class="popup-btn" onclick="reserverTele('${tele.nom}')">Réserver</button>`;
  }

  return `
    <b>${tele.nom}</b><br>
    Salle : ${tele.salle}<br>
    État : ${tele.etat}<br>
    ${actionButton}
  `;
}

function annulerReservation(nom) {
  const item = markersMap.get(nom);
  if (!item) return;

  item.tele.etat = "Fonctionnelle"; // ou "Disponible"
  item.marker.setStyle({ fillColor: "green" }); // couleur dispo

  const newPopup = generatePopupContent(item.tele);
  item.marker.setPopupContent(newPopup);

  alert(`❎ Réservation annulée pour la télé : ${nom}`);
}
