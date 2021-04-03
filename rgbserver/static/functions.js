$(document).ready(function () {
    $("#rainbow").click(() => $.get("/rainbow"))
    $("#rainbow-color-wipe").click(() => $.get("/rainbow_color_wipe"))
    $("#rainbow-fade").click(() => $.get("/rainbow_fade"))
    $("#random-fade").click(() => $.get("/random_fade"))
    $("#snake-color").click(() => $.get("/snake_color"))
    $("#snake-fade").click(() => $.get("/snake_fade"))
    $("#snake-rainbow").click(() => $.get("/snake_rainbow"))
    $("#strobe").click(() => $.get("/strobe"))
    $("#fire").click(() => $.get("/fire"))
    $("#clear").click(() => $.get("/clear"))

    const staticColor = new iro.ColorPicker("#static-color", {
        width: 200,
        color: "#fff",
        layout: [
            {
                component: iro.ui.Wheel,
                options: {}
            }
        ]
    })

    staticColor.on('input:end', function (color) {
        $.get(`/static_color/${color.red}/${color.green}/${color.blue}`)
    });

    const staticGradient = new iro.ColorPicker("#static-gradient", {
        width: 200,
        colors: ["#00f", "f00"],
        layout: [
            {
                component: iro.ui.Wheel,
                options: {}
            }
        ]
    })

    staticGradient.on('input:end', function () {
        let left = staticGradient.colors[0]
        let right = staticGradient.colors[1]
        $.get(`/static_gradient/${left.red}/${left.green}/${left.blue}/${right.red}/${right.green}/${right.blue}`)
    });
});
