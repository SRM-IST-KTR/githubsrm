import { useState } from "react";
import Link from "next/link";
import { Formik, Form } from "formik";
import Markdown from "react-markdown";

import { Section, Input } from "../";
import * as FormConstants from "../../../utils/constants";
import { LoadingIcon } from "../../../utils/icons";
import {
  AlphaMaintainerForm,
  BetaMaintainerForm,
} from "../../../utils/interfaces";
import { postMaintainer } from "../../../services/api";

const Maintainer = () => {
  let [stage, setStage] = useState<number>(0);
  let [loading, setLoading] = useState<boolean>(false);
  let [role, setRole] = useState<"alpha" | "beta" | null>(null);

  const alphaInitialValues: Partial<AlphaMaintainerForm> = {};
  const betaInitialValues: Partial<BetaMaintainerForm> = {};

  const submitValues = async (
    values: AlphaMaintainerForm | BetaMaintainerForm
  ) => {
    setLoading(true);
    try {
      const parsedValues = {
        ...values,
        tags: [values.tags.split(",").filter((i) => i.trim())],
      };
      const res = await postMaintainer(values, role);
    } catch (error) {
      console.log(error);
    }
    setLoading(false);
  };

  const changePage = (next: boolean) => {
    if (role === "alpha") {
      if (next) {
        if (stage !== FormConstants.alphaMaintainerInputs.length - 1)
          setStage(stage + 1);
      } else {
        if (stage !== 0) setStage(stage - 1);
      }
    } else {
      if (next) {
        if (stage !== FormConstants.betaMaintainerInputs.length - 1)
          setStage(stage + 1);
      } else {
        if (stage !== 0) setStage(stage - 1);
      }
    }
  };

  const errorInputId = (ids: string[], errors: string[]): boolean =>
    ids.some((id) => errors.includes(id));

  return (
    <div>
      <div>
        <div className="font-medium">
          <h1 className="text-4xl">Maintainer</h1>
          <h2 className="text-xl mt-2">descrip</h2>
        </div>

        <p className="text-right text-lg">
          Join us as a{" "}
          <Link href="/join-us/contributor">
            <a className="text-base-green font-bold hover:underline">
              Contributor
            </a>
          </Link>
        </p>
      </div>

      <Formik
        initialValues={
          role === "alpha"
            ? alphaInitialValues
            : role === "beta"
            ? betaInitialValues
            : null
        }
        onSubmit={submitValues}
        validationSchema={
          role === "alpha"
            ? FormConstants.alphaMaintainerValidation
            : role === "beta"
            ? FormConstants.betaMaintainerValidation
            : null
        }
      >
        {({ errors, touched }) => (
          <Form className="w-11/12 my-8 mx-auto">
            {role === null ? (
              <div className="text-center">
                <p className="text-lg">please choose your bid</p>

                <div className="grid grid-cols-3 w-8/12 mx-auto mt-8">
                  <button
                    onClick={() => setRole("beta")}
                    className="bg-base-teal text-white rounded-lg text-xl py-4 font-medium"
                  >
                    Existing Project
                  </button>
                  <span />

                  <button
                    onClick={() => setRole("alpha")}
                    className="bg-base-teal text-white rounded-lg text-xl py-4 font-medium"
                  >
                    New Project
                  </button>
                </div>
              </div>
            ) : role === "alpha" ? (
              <div className="flex justify-evenly">
                <div className="w-4/12 flex flex-col items-center justify-between min-h-lg border-r-2">
                  {FormConstants.alphaMaintainerInputs.map((item, index) => (
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
                    {FormConstants.alphaMaintainerInputs.map(
                      (section, index) => (
                        <div
                          key={section.inputs[0].id}
                          className={`${
                            stage !== index ? "hidden" : ""
                          } flex w-11/12 mx-auto flex-col`}
                        >
                          {section.inputs.map((field) => (
                            <Input
                              onError={Object.keys(errors)
                                .filter((i) => touched[i])
                                .includes(field.id)}
                              key={field.id}
                              {...field}
                              wrapperClassName={{
                                default: FormConstants.wrapperClassName,
                                onError: FormConstants.wrapperClassName,
                              }}
                              inputClassName={{
                                default: FormConstants.inputClassName,
                                onError: FormConstants.inputClassNameError,
                              }}
                              labelClassName={{
                                default: FormConstants.labelClassName,
                              }}
                            />
                          ))}
                        </div>
                      )
                    )}
                  </div>

                  <div className="w-11/12 mx-auto h-full pb-6 flex flex-col justify-end">
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

                  <div className="w-11/12 mx-auto grid grid-cols-3 gap-x-10 items-center justify-center">
                    <button
                      type="button"
                      onClick={() => {
                        setRole("beta");
                        setStage(0);
                      }}
                      className="bg-base-teal py-3 rounded-lg text-white font-medium"
                    >
                      Existing Project?
                    </button>
                    {stage == 0 ? (
                      <div />
                    ) : (
                      <button
                        type="button"
                        onClick={() => changePage(false)}
                        className="bg-base-smoke py-3 rounded-lg"
                      >
                        Back
                      </button>
                    )}

                    {stage !==
                    FormConstants.alphaMaintainerInputs.length - 1 ? (
                      <button
                        type="button"
                        onClick={() => changePage(true)}
                        className="text-white bg-base-black py-3 font-semibold rounded-lg"
                      >
                        Next
                      </button>
                    ) : (
                      <button
                        disabled={Object.keys(errors).length > 0}
                        type="submit"
                        className={`${
                          Object.keys(errors).length > 0
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
            ) : (
              <div className="flex justify-evenly">
                <div className="w-4/12 flex flex-col items-center justify-between min-h-lg border-r-2">
                  {FormConstants.betaMaintainerInputs.map((item, index) => (
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
                    {FormConstants.betaMaintainerInputs.map(
                      (section, index) => (
                        <div
                          key={section.inputs[0].id}
                          className={`${
                            stage !== index ? "hidden" : ""
                          } flex w-11/12 mx-auto flex-col`}
                        >
                          {section.inputs.map((field) => (
                            <Input
                              onError={Object.keys(errors)
                                .filter((i) => touched[i])
                                .includes(field.id)}
                              key={field.id}
                              {...field}
                              wrapperClassName={{
                                default: FormConstants.wrapperClassName,
                                onError: FormConstants.wrapperClassName,
                              }}
                              inputClassName={{
                                default: FormConstants.inputClassName,
                                onError: FormConstants.inputClassNameError,
                              }}
                              labelClassName={{
                                default: FormConstants.labelClassName,
                              }}
                            />
                          ))}
                        </div>
                      )
                    )}
                  </div>

                  <div className="w-11/12 mx-auto h-full pb-6 flex flex-col justify-end">
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

                  <div className="w-11/12 mx-auto grid grid-cols-3 gap-x-10 items-center justify-center">
                    <button
                      type="button"
                      onClick={() => {
                        setRole("alpha");
                        setStage(0);
                      }}
                      className="bg-base-teal py-3 rounded-lg text-white font-medium"
                    >
                      New Project?
                    </button>
                    {stage == 0 ? (
                      <div />
                    ) : (
                      <button
                        type="button"
                        onClick={() => changePage(false)}
                        className="bg-base-smoke py-3 rounded-lg"
                      >
                        Back
                      </button>
                    )}

                    {stage !== FormConstants.betaMaintainerInputs.length - 1 ? (
                      <button
                        type="button"
                        onClick={() => changePage(true)}
                        className="text-white bg-base-black py-3 font-semibold rounded-lg"
                      >
                        Next
                      </button>
                    ) : (
                      <button
                        disabled={Object.keys(errors).length > 0}
                        type="submit"
                        className={`${
                          Object.keys(errors).length > 0
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
            )}
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default Maintainer;
