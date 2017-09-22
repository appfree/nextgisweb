/* global define */
define([
    "dojo/_base/declare",
    "dojo/request/xhr",
    "./Adapter",
    "ngw/route",
    "ngw/openlayers/layer/VectorTile",
    "openlayers/ol",
    "mapbox-to-ol-style/mb2olstyle"
], function (declare, xhr, Adapter, route, VectorTile, ol, mb2olstyle) {
    return declare(Adapter, {
        createLayer: function (item) {
            var layer = new VectorTile(item.id, {
                visible: item.visibility,
                maxResolution: item.maxResolution ? item.maxResolution : undefined,
                minResolution: item.minResolution ? item.minResolution : undefined,
                opacity: item.transparency ? (1 - item.transparency / 100) : 1.0
            }, {
                format: new ol.format.MVT({
                    layerName: 'mvt-layer',
                    featureClass: ol.Feature
                }),
                tileGrid: ol.tilegrid.createXYZ(),
                tilePixelRatio: 16,
                wrapX: false,
                url: route.feature_layer.mvt(item.layerId, '{z}', '{x}', '{y}')
            });

            xhr.get(route.feature_layer.style(item.styleId), {
                handleAs: "json"
            }).then(
                function (style) {
                    if (Object.keys(style).length !== 0) {
                        mb2olstyle.default(ol,layer.olLayer, style, 'states');
                    }
                }
            );
            return layer;
    }});
});