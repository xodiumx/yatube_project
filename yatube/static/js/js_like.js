document.querySelectorAll('.heart-button').forEach(
    function (button) {
        return button.addEventListener(
            'click', function () {
                return button.classList.toggle('active');
            });
    });