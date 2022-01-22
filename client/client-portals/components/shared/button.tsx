import { ButtonWrapperProps } from "../../utils/interfaces";

export const STYLE = {
  primary: "text-white bg-base-teal p-3 min-w-32 font-semibold rounded-lg my-3",
  secondary:
    "flex justify-center w-1/8 mx-auto mt-4 bg-green-400 p-2 font-bold text-white rounded-xl",
  danger:
    "flex justify-center w-1/8 mx-auto mt-4 bg-red-600 p-2 font-bold text-white rounded-xl",
};

const Button = ({
  type,
  btnStyle,
  disabled,
  children,
  onClick,
}: ButtonWrapperProps) => {
  const checkButtonStyle =
    btnStyle in STYLE ? STYLE[btnStyle] : STYLE["secondary"];

  return (
    <button
      onClick={onClick}
      type={type}
      className={`${checkButtonStyle}`}
      disabled={disabled}
    >
      {children}
    </button>
  );
};

export default Button;
