


$(function() {

    var $form = $("#id_card_number").parents("form"),
        $back = $("#checkout_back"),
        $next = $("#checkout_next");

    $form.submit(function(e) {


        if($back.data("clicked") == "true"){
            return true;
        }

        if ( $("#id_card_number").is(":visible")) {
          var form = this;
          var card = {
            number:   $("#id_card_number").val(),
            expMonth: $("#id_card_expiry_month").val(),
            expYear:  $("#id_card_expiry_year").val(),
            cvc:      $("#id_card_cvv").val()
          };

          Stripe.createToken(card, function(status, response) {
            if (status === 200) {
              // console.log(status, response);
              $("#credit-card-errors").hide();
              $(".payment-errors").slideUp(250);
              $("#id_last_4_digits").val(response.card.last4);
              $("#id_stripe_token").val(response.id);
              form.submit();
              $("button[type=submit]").attr("disabled","disabled").html("Submitting..")
            } else {
              $(".payment-errors").text(response.error.message).slideDown(250);
              $("#user_submit").attr("disabled", false);
            }
          });

          return false;

        }

        return true

    });



    $back.on("click", function(e){
        $(this).data("clicked", "true");
    });

    $next.on("click", function(e) {
        $(this).data("clicked", "true");
    });
});

