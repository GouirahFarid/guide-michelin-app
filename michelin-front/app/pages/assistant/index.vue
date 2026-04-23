<template>
  <div class="flex flex-col items-center">
    <div class="w-full flex gap-x-4.5">
      <div class="bg-(--ui-michelin-red) p-3.75 flex w-fit rounded-full">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="white"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="m-auto lucide lucide-sparkles-icon lucide-sparkles"
        >
          <path
            d="M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z"
          />
          <path d="M20 2v4" />
          <path d="M22 4h-4" />
          <circle cx="4" cy="20" r="2" />
        </svg>
      </div>
      <div>
        <h2 class="text-xl font-bold">Assistant Michelin</h2>
        <span class="text-(--ui-michelin-dark-gray)">Toujours disponible</span>
      </div>
    </div>
  </div>
  <div class="flex flex-col items-center">
    <!-- <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="var(--ui-michelin-red)"
      stroke-width="2"
      stroke-linecap="round"
      stroke-linejoin="round"
      class="lucide lucide-arrow-left-icon lucide-arrow-left"
    >
      <path d="m12 19-7-7 7-7" />
      <path d="M19 12H5" />
    </svg> -->
    <h1 class="w-fit text-2xl font-bold">Que recherchez-vous ?</h1>
    <p class="w-fit text-(--ui-michelin-dark-gray)">
      Décrivez votre envie, je trouve l'adresse parfaite
    </p>
    <div class="max-w-125 flex gap-2.5 flex-wrap justify-center">
      <div
        class="w-fit py-2.5 px-5 border border-solid border-(--ui-michelin-light-gray) rounded-lg flex gap-x-2.5 cursor-pointer hover:outline hover:outline-solid hover:outline-(--ui-michelin-red)/70"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="var(--ui-michelin-red)"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="lucide lucide-map-pin-icon lucide-map-pin"
        >
          <path
            d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"
          />
          <circle cx="12" cy="10" r="3" />
        </svg>
        <span>Manger près de moi</span>
      </div>
      <div
        class="w-fit py-2.5 px-5 border border-solid border-(--ui-michelin-light-gray) rounded-lg flex gap-x-2.5 cursor-pointer hover:outline hover:outline-solid hover:outline-(--ui-michelin-red)/70"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="var(--ui-michelin-red)"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="lucide lucide-utensils-icon lucide-utensils"
        >
          <path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2" />
          <path d="M7 2v20" />
          <path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7" />
        </svg>
        <span>Bib Gourmand</span>
      </div>
      <div
        class="w-fit py-2.5 px-5 border border-solid border-(--ui-michelin-light-gray) rounded-lg flex gap-x-2.5 cursor-pointer hover:outline hover:outline-solid hover:outline-(--ui-michelin-red)/70"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="var(--ui-michelin-red)"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="lucide lucide-heart-icon lucide-heart"
        >
          <path
            d="M2 9.5a5.5 5.5 0 0 1 9.591-3.676.56.56 0 0 0 .818 0A5.49 5.49 0 0 1 22 9.5c0 2.29-1.5 4-3 5.5l-5.492 5.313a2 2 0 0 1-3 .019L5 15c-1.5-1.5-3-3.2-3-5.5"
          />
        </svg>
        <span>Date romantique</span>
      </div>
      <div
        class="w-fit py-2.5 px-5 border border-solid border-(--ui-michelin-light-gray) rounded-lg flex gap-x-2.5 cursor-pointer hover:outline hover:outline-solid hover:outline-(--ui-michelin-red)/70"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="var(--ui-michelin-red)"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="lucide lucide-wallet-icon lucide-wallet"
        >
          <path
            d="M19 7V4a1 1 0 0 0-1-1H5a2 2 0 0 0 0 4h15a1 1 0 0 1 1 1v4h-3a2 2 0 0 0 0 4h3a1 1 0 0 0 1-1v-2a1 1 0 0 0-1-1"
          />
          <path d="M3 5v14a2 2 0 0 0 2 2h15a1 1 0 0 0 1-1v-4" />
        </svg>
        <span>Petit Budget</span>
      </div>
      <div
        class="w-fit py-2.5 px-5 border border-solid border-(--ui-michelin-light-gray) rounded-lg flex gap-x-2.5 cursor-pointer hover:outline hover:outline-solid hover:outline-(--ui-michelin-red)/70"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="var(--ui-michelin-red)"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="lucide lucide-users-icon lucide-users"
        >
          <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
          <path d="M16 3.128a4 4 0 0 1 0 7.744" />
          <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
          <circle cx="9" cy="7" r="4" />
        </svg>
        <span>Dîner entre amis</span>
      </div>
      <div
        class="w-fit py-2.5 px-5 border border-solid border-(--ui-michelin-light-gray) rounded-lg flex gap-x-2.5 cursor-pointer hover:outline hover:outline-solid hover:outline-(--ui-michelin-red)/70"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="var(--ui-michelin-red)"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="lucide lucide-clock-icon lucide-clock"
        >
          <circle cx="12" cy="12" r="10" />
          <path d="M12 6v6l4 2" />
        </svg>
        <span>Dispo ce soir</span>
      </div>
    </div>

    <div class="w-full flex gap-2.5 p-3.75 items-center">
      <input
        type="text"
        placeholder="Un Bib gourmand sympa pour ce soir"
        class="grow bg-gray-100 placeholder:text-(--ui-michelin-dark-gray) rounded-lg py-2.5 px-5 outline-none focus:ring-1 focus:ring-(--ui-michelin-red) focus:ring-offset-1"
      />
      <div class="bg-(--ui-michelin-red) p-3 flex w-fit rounded-lg">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="white"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class="lucide lucide-send-icon lucide-send"
        >
          <path
            d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"
          />
          <path d="m21.854 2.147-10.94 10.939" />
        </svg>
      </div>
    </div>
  </div>
</template>
