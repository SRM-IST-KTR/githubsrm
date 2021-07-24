const STYLE = ["primary", "secondary"];

interface props {
  type?: "button" | "submit" | "reset";
  btnStyle?: "primary" | "secondary";
  disabled?: boolean;
  children?: JSX.Element | string;
  onClick?: (event?: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void;
}

const Button = ({ type, btnStyle, disabled, children, onClick }: props) => {
  const primary =
    "text-white bg-base-teal w-32 py-4 font-semibold rounded-lg my-3";
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
