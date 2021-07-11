import { Formik, Form } from "formik";
import Router from "next/router";

import { AdminLoginData } from "../../../utils/interfaces";
import {
  adminLoginValidation,
  adminLoginInputs,
} from "../../../utils/constants";
import { Input } from "../../shared";
import instance from "../../../services/api";
import { successToast, errToast } from "../../../utils/functions/toast";
import router from "next/router";

const AdminLogin = () => {
  const initialValues: AdminLoginData = {
    email: "",
    password: "",
  };

  const submitValues = (values: AdminLoginData) => {
    console.log(values);
    instance
      .post("admin/login", values)
      .then((res) => {
        console.log(res.data.keys);
        sessionStorage.setItem("token", res.data.keys);
        {
          /* //TODO: Remove this  */
        }
        sessionStorage.setItem("isLoggedIn", "1");
        successToast("Success");
        Router.push("admin/dashboard");
      })
      .catch((err) => {
        errToast("Authentication error!");
      });
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
        <Form className="flex flex-col px-6 lg:w-1/4 max-w-6xl mt-10 py-6 mx-auto bg-white rounded-lg">
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
