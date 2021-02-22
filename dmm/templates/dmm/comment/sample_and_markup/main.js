  $(document).ready(function () {

    $.ajax({
      url: "get_initials",
      type: "get",
      data: {
        expert_id: expert_id,
        tag_checked_ids: JSON.stringify([]),
        specie_checked_ids: JSON.stringify([]),
      },
      success: function (response) {
        $(".alert").alert("close");
        if (!is_result) {
          const now = new Date();
          now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
          document.getElementById("result-date").value = now.toISOString().slice(0, -1).substring(0, 16);
          refresh_comment_metas({
            result_tag_checked_ids: get_checked_ids($("#tags-section .tag")),
            result_language_type_selected: $("option:selected", $("#language-type")).attr("value")
          });
        }

        $("#tags-section").html(response.tags_section);
        $("#species-section").html(response.species_section);
        $("#comments-section").html(response.comments_section);

        refresh_comment_metas({});

        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        let forms = document.querySelectorAll(".needs-validation");

        // Loop over them and prevent submission
        Array.prototype.slice.call(forms).forEach(function (form) {
          form.addEventListener(
            "submit",
            function (event) {
              if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
              }
              form.classList.add("was-validated");
            },
            false
          );
        });
      },
      statusCode: {
        500: function () {
          alert(error_500_info);
        },
      },
    });

    // enable tooltips
    $(function () {
      $('[data-toggle="tooltip"]').tooltip();
    });

    // comment destroy clicked
    $("body").on("click", ".comment-destroy", function () {
      if (confirm("Вы уверены что хотите удалить комментарий?")) {
        // Standard confirmation message.
        let comment_instance_id = get_comment_instance_id($(this));
        // console.log('Trying destroy comment ' + comment_instance_id);
        $("#comment-instance-" + comment_instance_id).remove();
      }
    });

    // transfer data to each comment
    $("#transfer").click(function (e) {
      e.preventDefault();
      refresh_comment_metas({
        result_tag_checked_ids: get_checked_ids($("#tags-section .tag")),
        result_language_type_selected: $("option:selected", $("#language-type")).attr("value")
      });
    });

    // add tag
    $("#add-tag").click(function (e) {
      if (confirm("Вы уверены что хотите добавить тег?")) {
        // Standard confirmation message.
        if (!document.getElementById("add-tag-form").checkValidity()) {
          alert("Не все поля заполнены!");
          return;
        }
        e.preventDefault();
        $.ajax({
          url: "add_tag",
          type: "post",
          data: {
            tag_expert_id: expert_id,
            tag_name: $("#tag-name").val(),
            tag_description: $("#tag-description").val(),
            tag_is_common: !!$("#tag-is-common").is(":checked"),
            tag_checked_ids: JSON.stringify(get_checked_ids($(".tag"))),
            csrfmiddlewaretoken: csrf,
          },
          success: function (response) {
            $("#tags-section").html(response.tags_section);
            refresh_comment_metas({});
            $("#add-tag-form").trigger("reset");
          },
          statusCode: {
            500: function () {
              alert(error_500_info);
            },
          },
        });
      } else {
        // Pressed Cancel.
      }
    });

    // add specie
    $("#add-specie").click(function (e) {
      if (confirm("Вы уверены что хотите добавить класс?")) {
        // Standard confirmation message.
        if (!document.getElementById("add-specie-form").checkValidity()) {
          alert("Не все поля заполнены!");
          return;
        }
        e.preventDefault();
        $.ajax({
          url: "add_specie",
          type: "post",
          data: {
            specie_expert_id: expert_id,
            specie_name: $("#specie-name").val(),
            specie_description: $("#specie-description").val(),
            specie_checked_ids: JSON.stringify(get_checked_ids($(".specie"))),
            csrfmiddlewaretoken: csrf,
          },
          success: function (response) {
            $("#species-section").html(response.species_section);
            refresh_comment_metas({});
            $("#add-specie-form").trigger("reset");
          },
          statusCode: {
            500: function () {
              alert(error_500_info);
            },
          },
        });
      } else {
        // Pressed Cancel.
      }
    });

    // add comment
    $("#add-comment").click(function (e) {
      e.preventDefault();
      let tag_checked_ids = get_result_tag_checked_ids();
      let specie_checked_ids = get_result_specie_checked_id();
      let tonal_type_checked_ids = [];
      let last_comment_id = get_last_comment_id();
      let last_comment_date = get_last_comment_date();
      let language_type_selected = null;
      $.ajax({
        url: "add_comment",
        type: "get",
        data: {
          last_comment_id: last_comment_id,
        },
        success: function (response) {
          $("#comments-section").append(response.body);
          replace_comment_meta({
            tag_checked_ids: tag_checked_ids,
            specie_checked_ids: specie_checked_ids,
            tonal_type_checked_id: tonal_type_checked_ids,
            language_type_selected: language_type_selected,
            destination: $("#comment-meta-" + (parseInt(last_comment_id) + 1) + " > .card"),
            comment_instance_id: parseInt(last_comment_id) + 1,
            comment_date: last_comment_date,
            comment_is_answer: "false",
            author_url_value: ''
          });
        },
        statusCode: {
          500: function () {
            alert(error_500_info);
          },
        },
      });
    });

    // confirm-tagging
    $("#finish-comment-round").click(function (e) {
      if (confirm("Вы уверены что хотите закончить раунд?")) {
        // Standard confirmation message.
        if (!document.getElementById("round-form").checkValidity()) {
          alert("Не все поля заполнены!");
          return;
        }
        e.preventDefault();
        $.ajax({
          url: "insert_result",
          type: "post",
          data: {
            text: '',
            title: get_result_title_val(),
            url: get_result_url_val(),
            language_type_id: get_result_language_type_id(),
            resource_type_id: get_result_resource_type_selected_id(),
            content_type_id: get_result_content_type_selected_id(),
            result_date: get_result_date_val(),
            expert_id: expert_id,
            csrfmiddlewaretoken: csrf,
          },
          success: function (response) {
            $(".comment").each(function (i, obj) {
              let target = $(this);
              $.ajax({
                url: "insert_comment",
                type: "post",
                data: {
                  comment_text: get_comment_text_val(target),
                  author_url: get_comment_author_url_val(target),
                  result_id: response.result_id,
                  is_answer: get_comment_is_answer(target),
                  language_type_id: get_result_language_type_id(),
                  resource_type_id: get_result_resource_type_selected_id(),
                  comment_date: get_last_comment_date(target),
                  expert_id: expert_id,
                  csrfmiddlewaretoken: csrf,
                },
                success: function (response) {
                  $.ajax({
                    url: "insert_comment_round",
                    type: "post",
                    data: {
                      comment_id: response.comment_id,
                      specie_id: get_comment_specie_checked_id(target),
                      tag_ids: JSON.stringify(get_comment_tag_checked_ids(target)),
                      tonal_type_id: get_comment_tonal_type_checked_id(target),
                      clarification: get_comment_clarification_val(target),
                      expert_id: expert_id,
                      csrfmiddlewaretoken: csrf,
                    },
                    success: function (response) {
                      let comment_round_id = response.comment_round_id;
                      $("#round-form").trigger("reset");
                      alert("УСПЕХ!");
                    },
                    statusCode: {
                      500: function () {
                        alert(error_500_info);
                      },
                    },
                  });
                },
              });
            });
          },
          statusCode: {
            500: function () {
              alert(error_500_info);
            },
          },
        });
      } else {}
    });
  });