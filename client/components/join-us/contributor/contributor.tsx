import { useState } from "react";
import Link from "next/link";
import { Formik, Form, FormikState } from "formik";
import Markdown from "react-markdown";

import { Section } from "../";
import { Input } from "../../shared";
import {
  contributorInputs,
  contributorValidation,
  customInputClasses,
} from "../../../utils/constants";
import { LoadingIcon } from "../../../utils/icons";
import { ContributorFormData } from "../../../utils/interfaces";
import { postContributor } from "../../../services/api";
import { getUser } from "../../../services/validate";
import { successToast } from "../../../utils/functions/toast";

const Contributor = () => {
  const [stage, setStage] = useState<number>(0);
  const [loading, setLoading] = useState<boolean>(false);

  //@ts-ignore
  const initialValues: ContributorFormData = {
    name: "",
    email: "",
    github_id: "",
    srm_email: "",
    reg_number: "",
    branch: "",
    interested_project: "",
    poa: "",
  };

  const submitValues = async (
    values: ContributorFormData,
    setErrors: (errors: Partial<ContributorFormData>) => void,
    resetForm: (nextState?: Partial<FormikState<ContributorFormData>>) => void
  ) => {
    setLoading(true);
    if (await getUser(values.github_id)) {
      const res = await postContributor(values);
      if (res) {
        successToast("Registered as a Contributor!");
        setStage(0);
        resetForm({ values: { ...initialValues } });
        setLoading(false);
        return;
      }
    } else {
      setErrors({
        github_id: "**GitHub ID**: Invalid",
      } as Partial<ContributorFormData>);
      setLoading(false);
      return;
    }
    setLoading(false);
  };

  const changePage = (next: boolean) => {
    if (next) {
      if (stage !== contributorInputs.length - 1) setStage(stage + 1);
    } else {
      if (stage !== 0) setStage(stage - 1);
    }
  };

  const errorInputId = (ids: string[], errors: string[]): boolean =>
    ids.some((id) => errors.includes(id));

  return (
    <div>
      <div>
        <div className="font-medium">
          <h1 className="text-2xl lg:text-4xl">Contributor</h1>
          <h2 className="lg:text-xl lg:mt-2">
            Please fill the details correctly.
          </h2>
        </div>

        <p className="lg:text-right lg:text-lg mt-2 lg:mt-0">
          Join us as a{" "}
          <Link href="/join-us/maintainer">
            <a className="text-base-green font-bold hover:underline">
              Maintainer
            </a>
          </Link>
        </p>
      </div>

      <Formik
        initialValues={initialValues}
        onSubmit={(values, { setErrors, resetForm }) =>
          submitValues(values as ContributorFormData, setErrors, resetForm)
        }
        validationSchema={contributorValidation}
      >
        {({ errors, touched }) => (
          <Form className="w-11/12 my-8 mx-auto">
            <>
              <div className="flex justify-evenly flex-col lg:flex-row">
                <div className="w-full lg:w-4/12 flex flex-col items-start lg:items-center justify-between lg:min-h-lg  lg:border-r-2 lg:border-t-0 mb-12">
                  {contributorInputs.map((item, index) => (
                    <Section
                      key={item.section}
                      name={item.section}
                      description={item.description}
                      icon={item.icon}
                      isActive={stage === index}
                      setActive={() => setStage(index)}
                      onError={errorInputId(
                        item.inputs.map((i) => i.id),
                        Object.keys(errors).filter((i) => touched[i])
                      )}
                    />
                  ))}
                </div>

                <div className="w-full max-w-3xl flex flex-col justify-between">
                  <div>
                    {contributorInputs.map((section, index) => (
                      <div
                        key={section.inputs[0].id}
                        className={`${
                          stage !== index ? "hidden" : ""
                        } flex w-11/12 mx-0 lg:mx-auto flex-col`}
                      >
                        {section.inputs.map((field) => (
                          <Input
                            onError={Object.keys(errors)
                              .filter((i) => touched[i])
                              .includes(field.id)}
                            key={field.id}
                            {...field}
                            {...customInputClasses}
                          />
                        ))}
                      </div>
                    ))}
                  </div>

                  <div className="w-11/12  mx-auto h-full pb-6 flex flex-col justify-end">
                    {Object.keys(errors).map((error) => {
                      if (touched[error]) {
                        return (
                          <Markdown
                            key={error.trim()}
                            className="text-red-500 my-1"
                          >
                            {errors[error] as string}
                          </Markdown>
                        );
                      }
                    })}
                  </div>

                  <div>
                    <div className="w-11/12 mx-auto grid grid-rows-3 lg:grid-rows-none lg:grid-cols-3 grid-flow-row lg:grid-flow-col gap-5 gap-x-10 justify-items-auto">
                      <div className=" w-full py-3" />
                      {stage == 0 ? (
                        <div className=" w-full py-3" />
                      ) : (
                        <button
                          type="button"
                          onClick={() => changePage(false)}
                          className="bg-base-smoke w-full py-3 rounded-lg"
                        >
                          Back
                        </button>
                      )}

                      {stage !== contributorInputs.length - 1 ? (
                        <button
                          type="button"
                          onClick={() => changePage(true)}
                          className="text-white  bg-base-black py-3 font-semibold rounded-lg"
                        >
                          Next
                        </button>
                      ) : (
                        <button
                          disabled={Object.keys(errors).length > 0 || loading}
                          type="submit"
                          className={`${
                            Object.keys(errors).length > 0 || loading
                              ? "cursor-not-allowed bg-opacity-70"
                              : "cursor-pointer"
                          } text-white bg-base-green py-3 font-semibold rounded-lg`}
                        >
                          {!loading ? (
                            "Submit"
                          ) : (
                            <span className="flex w-6 mx-auto">
                              <LoadingIcon />
                            </span>
                          )}
                        </button>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default Contributor;
