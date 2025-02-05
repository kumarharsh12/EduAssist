"use client";

import { CardBody, CardContainer, CardItem } from "@/app/components/ui/3d-card";
import Image from "next/image";
import Link from "next/link";
import React from "react";

export function ThreeDCardDemo() {
  return (
    <CardContainer className="flex flex-col items-center py-2">
      <CardBody className="max-w-3xl text-center p-6 bg-white rounded-2xl shadow dark:bg-gray-100 dark:bg-opacity-5 flex flex-col items-center">
        <CardItem
          translateZ="50"
          className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white"
        >
          Introducing
        </CardItem>
        <CardItem
          as="p"
          translateZ="60"
          className="text-6xl font-bold tracking-tight text-gray-900 dark:text-white"
        >
          EduAssist
        </CardItem>
        <div className="flex justify-center items-center mt-4">
          <Link href="/Upload">
            <CardItem
              translateZ={20}
              as="button"
              className="shadow-2xl inline-flex items-center px-5 py-4 text-base font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
            >
              Get Started
            </CardItem>
          </Link>
        </div>
        <CardItem
          as="p"
          translateZ="40"
          className="mb-3 my-3 font-normal text-gray-700 dark:text-gray-400 text-center"
        >
          We’ve developed a model called EduAssist, designed specifically to
          support educators and learners in an interactive, dynamic environment.
          The model processes educational content namely text content and audio
          files adapting to various subjects and teaching styles to offer
          tailored assistance. EduAssist can summarize key concepts, clarify
          complex ideas, and provide interactive explanations to ensure deeper
          understanding.
        </CardItem>
        <CardItem
          as="p"
          translateZ="40"
          className="mb-3 font-normal text-gray-700 dark:text-gray-400 text-center"
        >
          It can engage in dialogue with users, adjusting its explanations based
          on feedback, and offer a variety of study aids .EduAssist is built to
          enhance both teaching and learning experiences by making educational
          content more accessible, engaging, and effective for a wide range of
          learners.
        </CardItem>
      </CardBody>
    </CardContainer>
  );
}
