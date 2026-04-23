<!-- <template>
  <div class="mx-2.5 mt-5">
    <div>
      <h1>Créateurs</h1>
      <p>Les voix food qui comptent</p>
    </div>
    <div>
      <h2>Créateurs certifiés Michelin</h2>
      <div>
        <div>
          <div class="relative w-full h-20"></div>
          <div>
            <div
              class="w-10 h-10 absolute rounded-full bg-red-500 -bottom-1/2"
            ></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template> -->
<template>
  <div class="min-h-screen bg-gray-50 pb-24">
    <header class="p-6 max-w-5xl mx-auto">
      <h1 class="text-4xl font-serif font-bold text-gray-900">Créateurs</h1>
      <p class="text-gray-500 mt-1">Les voix food qui comptent</p>

      <h2 class="text-lg font-bold text-gray-900 mt-8 mb-4">
        Créateurs certifiés Michelin
      </h2>
    </header>

    <main class="px-6 max-w-5xl mx-auto">
      <CreatorCard
        name="Sophie Laurent"
        handle="@sophie.tables"
        specialty="Accords mets-vins & gastronomie"
        bio="Ex-sommelière reconvertie créatrice de contenu. Mes adresses préférées, avec accord mets-vins."
        followers="67.8k"
        lists="15"
        avatar="https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=200&h=200&fit=crop"
        banner="https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=1000&fit=crop"
      />

      <CreatorCard
        name="Margaux Delacroix"
        handle="@margaux.food"
        specialty="Bib Gourmand & bistrots"
        bio="Chroniqueuse food à Paris. Bib Gourmand addict. Je déniche les pépites pour que vous n'ayez plus à chercher."
        followers="42k"
        lists="12"
        avatar="https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=200&h=200&fit=crop"
        banner="https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=1000&fit=crop"
      />
    </main>

    <nav
      class="fixed bottom-0 w-full bg-white border-t border-gray-200 px-6 py-3 flex justify-around items-center"
    >
      <NavItem icon="home" label="Accueil" />
      <NavItem icon="search" label="Explorer" />
      <NavItem icon="chat" label="Assistant" />
      <NavItem icon="users" label="Créateurs" active />
      <NavItem icon="user" label="Profil" />
    </nav>
  </div>
</template>

<style>
/* Importation d'une police Serif pour le style Michelin */
@import url("https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap");

h1 {
  font-family: "Playfair Display", serif;
}
</style>
