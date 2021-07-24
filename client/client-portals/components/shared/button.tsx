import { ButtonWrapperProps } from "../../utils/interfaces";

const STYLE = ["primary", "secondary"];

const Button = ({
  type,
  btnStyle,
  disabled,
  children,
  onClick,
}: ButtonWrapperProps) => {
  const primary =
    "text-white bg-base-teal p-3 min-w-32 font-semibold rounded-lg my-3";
  const secondary =
    "flex justify-center w-1/8 mx-auto mt-4 bg-green-400 p-2 font-bold text-white rounded-xl";

  const checkButtonStyle = STYLE.includes(btnStyle) ? primary : secondary;

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
