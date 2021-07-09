import { Formik, Form } from "formik";

import { AdminLoginData } from "../../../utils/interfaces";
import {
  adminLoginValidation,
  adminLoginInputs,
} from "../../../utils/constants";
import { Input } from "../../shared";

const AdminLogin = () => {
  const initialValues: AdminLoginData = {
    email: "",
    password: "",
  };

  const submitValues = (values: AdminLoginData) => {
    console.log(values);
  };

  return (
    <div className="min-h-screen p-14 bg-base-blue">
      <h1 className="flex justify-center text-4xl font-extrabold text-white">
        Admin Login
      </h1>

      <Formik
        initialValues={initialValues}
        onSubmit={submitValues}
        validationSchema={adminLoginValidation}
      >
        <Form className="flex flex-col px-6 w-1/4 max-w-6xl mt-10 py-6 mx-auto bg-white rounded-lg">
          {adminLoginInputs.map((input) => (
            <div className="border-2 border-gray-700 rounded my-4 p-4">
              <Input key={input.id} {...input} />
            </div>
          ))}
          <div className="flex justify-center">
            <button
              type="submit"
              className="rounded-xl font-bold items-center my-3 bg-base-teal p-3"
            >
              Log In
            </button>
          </div>
        </Form>
      </Formik>
    </div>
  );
};

export default AdminLogin;
