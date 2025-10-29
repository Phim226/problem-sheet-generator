from sympy import Add, Expr, S, latex

I_HAT_LATEX = r"\mathbf{{\hat{{i}}}}"
J_HAT_LATEX = r"\mathbf{{\hat{{j}}}}"
K_HAT_LATEX = r"\mathbf{{\hat{{k}}}}"

def format_component_latex(
          component: Expr,
          is_x_component: bool = False
) -> str:
    """
    Format the latex for a component of the vector function.

    Parameters
    =========
    component: Expr
        The sympy expression object of the component being formatted.

    is_x_component: bool, optional
        If the component is the x component then no leading + sign is added.
        Default is False.

    Returns
    ======
    str
        The formated LaTeX string for the vector function component.
    """
    if component is S.NegativeOne:
        return "-"
    elif component is S.One:
        return "+"
    elif component is S.Zero:
        return None
    elif isinstance(component, Add):
        return rf"{"+"}\left({latex(component)}\right)"

    component_latex = latex(component)
    if is_x_component:
         return component_latex
    return f"{"+" + component_latex if component_latex[0] != "-" else component_latex}"

def format_vector_function_latex(
            x_latex: str,
            y_latex: str,
            z_latex: str
    ) -> str:
        """
        Format the LaTeX for a vector function expression.

        Parameters
        =========
        x_latex: str
            LaTeX for the x component of the vector function.

        y_latex: str
            LaTeX for the y component of the vector function.

        z_latex: str
            LaTeX for the z component of the vector function.

        Returns
        ======
        str
            The LaTeX of the vector function.
        """
        vector_latex: str = (
            f"{x_latex + I_HAT_LATEX if x_latex is not None else ""}"
            f"{y_latex + J_HAT_LATEX if y_latex is not None else ""}"
            f"{z_latex + K_HAT_LATEX if z_latex is not None else ""}"
        )

        if vector_latex[0] == "+":
            vector_latex = vector_latex[1:]

        return vector_latex