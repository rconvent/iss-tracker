<template>
                <div id="map-container">
                    <div id="map"></div>
                                            <div class="calculation-box">
                                                <p>Click the map to draw a polygon.</p>
                                                <div id="calculated-area"></div>
                                            </div>
                                    </div>
</template>
<script>
import MapboxDraw from "@mapbox/mapbox-gl-draw";
import mapboxgl from 'mapbox-gl';

import 'mapbox-gl/dist/mapbox-gl.css';

export default {
    data() {
        return {
            accessToken:
                'pk.eyJ1IjoicmNvbnZlbnQiLCJhIjoiY2xodXB3eXI1MDI4OTNncGdpY2E4MndzZyJ9.4Cm9FftoMvjqw8xJf6DJGw',
            map: {},
        }
    },
    mounted() {
        this.createMap()
    },

    methods: {
        createMap() {
            mapboxgl.accessToken = this.accessToken
            const map = new mapboxgl.Map({
                container: 'map',
                style: 'mapbox://styles/mapbox/streets-v12',
                zoom: 2,
            })

            map.on('load', async () => {
                const geojson = await getLocation()
                map.addSource('iss', {
                    type: 'geojson',
                    data: geojson,
                })

                map.addLayer({
                    id: 'iss_position',
                    type: 'symbol',
                    source: 'iss',
                    layout: {
                        'icon-image': 'rocket',
                    },
                })

                const popup = new mapboxgl.Popup({
                    closeButton: false,
                    closeOnClick: false
                });

                map.on('mouseenter', 'iss_position', (e) => {
                    map.getCanvas().style.cursor = 'pointer'

                    const coordinates = e.features[0].geometry.coordinates.slice()
                    const sunExposure = e.features[0].properties.sunExposure

                    while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
                        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360
                    }


                    popup.setLngLat([coordinates[0], coordinates[1]])
                        .setHTML(
                            `${sunExposure}`
                        )
                        .addTo(map)
                })

                map.on('mouseleave', 'iss_position', () => {
                    map.getCanvas().style.cursor = ''
                    popup.remove()
                })

                const updateSource = setInterval(async () => {
                    const geojson = await getLocation(updateSource)
                    map.getSource('iss').setData(geojson)
                }, 20000)

                const draw = new MapboxDraw({
                    displayControlsDefault: false,
                    controls: {
                        polygon: true,
                        trash: true
                    },
                    defaultMode: 'draw_polygon'
                });
                map.addControl(draw);

                map.on('draw.create', sendArea);

                async function sendArea(e) {

                    const data = draw.getAll();
                    const lastDraw = data.features[data.features.length - 1]
                    const jsonData = {
                        "mapbox_uuid": lastDraw.id,
                        "type": "Feature",
                        "geometry": lastDraw.geometry,
                        "properties": lastDraw.properties
                    }
                    console.log(JSON.stringify(jsonData))

                    console.log(jsonData)
                    const response = await fetch("http://0.0.0.0:8000/geojson/", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(jsonData),
                    })
                }

                async function getLocation(updateSource) {
                    try {
                        const positionResponse = await fetch(
                            'http://0.0.0.0:8000/iss/position/',
                            { method: 'GET' }
                        )
                        const { latitude, longitude } = await positionResponse.json()

                        var dayBefore = new Date()
                        dayBefore.setDate(dayBefore.getDate() - 1)
                        dayBefore = dayBefore.toISOString().split('T')[0]
                        const exposureResponse = await fetch(
                            `http://0.0.0.0:8000/iss/sun/?from_date=${dayBefore}`,
                            { method: 'GET' }
                        )
                        const sunExposure = await exposureResponse.json()


                        map.flyTo({
                            center: [longitude, latitude],
                            speed: 0.5,
                        })

                        return {
                            type: 'FeatureCollection',
                            features: [
                                {
                                    type: 'Feature',
                                    geometry: {
                                        type: 'Point',
                                        coordinates: [longitude, latitude],
                                    },
                                    properties: {
                                        sunExposure:
                                            `<h1>ISS Sun Exposure : </h1>
                                            <ul>
                                            ${sunExposure.map((interval) => `<li>${interval}</li>`).join('')}
                                            </ul>
                                            `,
                                    },
                                },
                            ],
                        }
                    } catch (err) {
                        if (updateSource) clearInterval(updateSource)
                        throw new Error(err)
                    }
                }
            })
        },
    },
}
</script>

<style>
#map-container {
    position: relative;
    width: 100%;
    height: 100vh;
}

#map {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
}

.mapboxgl-popup {
    position: absolute;
    max-width: 400px;
    font: 12px/20px 'Helvetica Neue', Arial, Helvetica, sans-serif;
}

.calculation-box {
    height: 75px;
    width: 150px;
    position: absolute;
    bottom: 40px;
    left: 10px;
    background-color: rgba(255, 255, 255, 0.9);
    padding: 15px;
    text-align: center;
}
 
p {
    font-family: 'Open Sans';
    margin: 0;
    font-size: 13px;
}
</style>