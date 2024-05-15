
import parsel

from utils import shrink_list


def _to_div(html):  # old
    match html:
        case parsel.Selector():
            return html
        case str():
            selector = parsel.Selector(html)
            if isinstance(selector, parsel.Selector):
                return selector
    raise TypeError


def _parse_mode(div_tem, mode):  # old
    match mode:
        case "div":
            return div_tem
        case "content":
            return shrink_list(div_tem.getall())
        case "text":
            div_tem = div_tem.css("::text")
            return shrink_list(div_tem.getall())
        case _:
            raise ValueError(f"invalid mode: '{mode}'")


def html_parse(html: str | parsel.Selector, csss: str | list | dict, mode="default"):  # old
    div = _to_div(html)
    match csss:
        case str():
            div = div.css(csss)
            mode = "text" if mode == "default" else mode
            return _parse_mode(div, mode=mode)
        case list():
            mode = "content" if mode == "default" else mode
            for cs in csss:
                div = div.css(cs)
            return _parse_mode(div, mode=mode)
        case dict():
            tem_dict = dict()
            for key, cs in csss.items():
                tem_dict[key] = html_parse(div, cs, mode=mode)
            print(tem_dict)
            return tem_dict
        case _:
            raise TypeError


def html_parses_struct(html: str | parsel.Selector, csss_list):  # old
    div = _to_div(html)
    if len(csss_list) == 1:
        csss = csss_list[0]
        return html_parse(div, csss)
    else:
        cs = csss_list[0]
        if not isinstance(cs, str):
            raise TypeError
        data_list = list()
        divs = div.css(cs)
        for div in divs:
            data_list.append(html_parses_struct(div, csss_list[1:]))
        return data_list


# rebuild
def _to_selector(func):
    def wrapper(html, *args, **kwargs):
        match html:
            case parsel.Selector():
                selector = html
            case str():
                selector = parsel.Selector(html)
                if not isinstance(selector, parsel.Selector):
                    raise TypeError("html can't be convert to selector")
            case _:
                raise TypeError("html is neither selector nor str")
        return func(selector, *args, **kwargs)
    return wrapper


def _html_parse_base_css(selector, css_str, isfinal=False):
    assert isinstance(css_str, str)
    selector = selector.css(css_str)
    if isfinal:
        return selector.getall()
    else:
        return selector


def _html_parse_base_css_list(selector, css_list):
    assert isinstance(css_list, list)
    for css in css_list:
        selector = selector.css(css)
    return selector


def _html_parse_base_css_or_css_list(selector, css_or_css_list):
    match css_or_css_list:
        case str():
            return _html_parse_base_css(selector, css_or_css_list)
        case list():
            return _html_parse_base_css_list(selector, css_or_css_list)
        case _:
            raise TypeError


def _html_parse_base_css_dict(selector, css_dict):
    assert isinstance(css_dict, dict)
    data_dict = dict()
    for key, css_dyt in css_dict.items():
        data_dict[key] = _html_parse_base_css_or_css_list(selector, css_dyt)
    return data_dict


@_to_selector
def base_css(html, css):
    return _html_parse_base_css(html, css)


@_to_selector
def base_css_list(html, css_list):
    return _html_parse_base_css_list(html, css_list)


@_to_selector
def base_css_dict(html, css_dict):
    return _html_parse_base_css_dict(html, css_dict)


@_to_selector
def base_css_dyt(html, css_dyt):
    match css_dyt:
        case str():
            return _html_parse_base_css(html, css_dyt)
        case list():
            return _html_parse_base_css_list(html, css_dyt)
        case dict():
            return _html_parse_base_css_dict(html, css_dyt)
        case _:
            raise TypeError(f"type {css_dyt} should be str, list or dict")
