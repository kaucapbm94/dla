  let error_500_info = "Что-то пошло не так, свяжитесь с администратором!";

  function get_checked_ids(iterator) {
    ids_list = [];
    iterator.each(function (i, obj) {
      if (obj.checked === true) ids_list.push(obj.value);
    });
    return ids_list;
  }

  function get_comment_instance_id(target) {
    let s = target.attr("id");
    return s.substr(s.lastIndexOf("-") + 1);
  }

  function get_result_date_val() {
    return $("#result-date").val();
  }

  function get_result_content_type_selected_id() {
    return $("option:selected", $("#content-type")).attr("value");
  }

  function get_result_resource_type_selected_id() {
    return $("option:selected", $("#resource-type")).attr("value");
  }

  function get_result_title_val() {
    return $("#title-input").val();
  }

  function get_last_comment_date(target) {
    return $("#comment-date-" + get_comment_instance_id(target)).val()
  }

  function get_result_url_val() {
    return $("#url-input").val();
  }

  function get_comment_text_val(target) {
    console.log(get_comment_instance_id(target));
    return $("#comment-text-" + get_comment_instance_id(target)).val();
  }

  function get_comment_author_url_val(target) {
    return $("#comment-author-url-" + get_comment_instance_id(target)).val();
  }

  function get_comment_is_answer(target) {
    return $("#comment-is-answer-" + get_comment_instance_id(target)).is(":checked")
  }

  function get_result_language_type_id() {
    return $("option:selected", $("#language-type")).attr("value");
  }


  function get_last_comment_date() {
    comment_date = $(".comment-meta .datetime-local").last().val();
    if (comment_date == "" || comment_date === undefined) {
      comment_date = $("#result-date").val();
    }
    return comment_date;
  }

  function get_last_comment_id() {
    last_comment_id = 0;
    try {
      last_comment_id = $(".comment").last().attr("id").replace(/comment-instance-/i, "");
    } catch (TypeError) {
      last_comment_id = 0;
    }
    let last_comment_date = get_last_comment_date()
    return last_comment_id;
  }

  function get_comment_specie_checked_id(target) {
    return get_checked_ids($("#comment-meta-" + get_comment_instance_id(target) + " .specie"))[0]
  }

  function get_comment_tag_checked_ids(target) {
    return get_checked_ids($("#comment-meta-" + get_comment_instance_id(target) + " .tag"));
  }

  function get_comment_tonal_type_checked_id(target) {
    return get_checked_ids($("#comment-meta-" + get_comment_instance_id(target) + " .tonal-type"))[0]
  }

  function get_comment_clarification_val(target) {
    return $("#comment-meta-" + get_comment_instance_id(target) + " .clarification").val()
  }

  function get_comment_date_val(target) {
    return $("#comment-date-" + get_comment_instance_id(target)).val() || $("#result-date").val();
  }


  function get_comment_author_url(target) {
    return $("#comment-author-url-" + get_comment_instance_id(target)).val()
  }

  function get_comment_language_type_selected(target) {
    return $("option:selected", $("#language-type-" + get_comment_instance_id(target))).attr("value");
  }

  function get_result_specie_checked_id() {
    return get_checked_ids($("#species-section .specie"));
  }

  function get_result_tag_checked_ids() {
    return get_checked_ids($("#tags-section .tag"));
  }



  function refresh_comment_metas({
    result_tag_checked_ids = null,
    result_language_type_selected = null
  }) {
    // iterate through each comment instance
    $(".comment-meta").each(function (i, obj) {
      let my_id = $(this).attr("id");
      let comment_instance_id = my_id.replace(/comment-meta-/i, "");
      replace_comment_meta({
        tag_checked_ids: result_tag_checked_ids || get_comment_tag_checked_ids($(this)),
        specie_checked_ids: get_result_specie_checked_id(),
        tonal_type_checked_id: get_comment_tonal_type_checked_id($(this)),
        language_type_selected: result_language_type_selected || get_comment_language_type_selected($(this)),
        destination: $("#" + my_id + " > .card"),
        comment_instance_id: get_comment_instance_id($(this)),
        comment_date: get_comment_date_val($(this)),
        comment_is_answer: get_comment_is_answer($(this)),
        author_url_value: get_comment_author_url($(this))
      });
    });
  }

  function replace_comment_meta({
    tag_checked_ids,
    specie_checked_ids,
    tonal_type_checked_ids,
    language_type_selected,
    destination,
    comment_instance_id,
    comment_date,
    comment_is_answer,
    author_url_value = null
  }) {
    $.ajax({
      url: "get_comment_meta",
      type: "get",
      data: {
        comment_instance_id: comment_instance_id,
        author_url_value: author_url_value,
        specie_checked_ids: JSON.stringify(specie_checked_ids),
        tag_checked_ids: JSON.stringify(tag_checked_ids),
        tonal_type_checked_ids: JSON.stringify(tonal_type_checked_ids),
        language_type_selected: language_type_selected,
        comment_date: comment_date,
        comment_is_answer: comment_is_answer,
      },
      success: function (response) {
        destination.replaceWith(response.body);
      },
      statusCode: {
        500: function () {
          alert(error_500_info);
        },
      },
    });
  }