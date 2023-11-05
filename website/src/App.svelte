<script>
  import { Styles, Button } from "sveltestrap";

  async function get_installer_link() {
    let installerlink = (
      await (await fetch("https://api.github.com/repos/modern-modpacks/pissmc/releases")).json()
    ).filter(x => x.tag_name.startsWith("i("))[0].html_url
    return installerlink
  }
</script>

<Styles />

<main>
  <div class="text-center bg-secondary text-white py-5">
    <img class="h-25 w-25 mx-auto" draggable="false" src="https://user-images.githubusercontent.com/79367505/270132869-44149f1d-76f5-402c-a4af-0c7dc29f86c7.png" alt="logo">
    <h1 class="fw-bold mt-4">PissMC</h1>
    <h2>Beyond classic</h2>

    <div class="d-flex gap-3 justify-content-center mt-4">
      {#await get_installer_link()}
        <Button color="success">Get PissMC</Button>
      {:then link}
        <a href="{link}">
          <Button color="success">Get PissMC</Button>
        </a>
      {/await}
      <a href="https://pissrinth.modernmodpacks.site">
        <Button color="info">Pissrinth (BUTTON DOESN'T WORK IGNORE)</Button>
      </a>
      <a href="https://wiki.modernmodpacks.site/wiki/misc/pissmc">
        <Button color="light">Read the docs</Button>
      </a>
    </div>
  </div>

  <div class="d-flex justify-content-around pb-3">
    <div class="h-25 w-25 text-center">
      <img class="h-100 w-100" draggable="false" src="https://img.freepik.com/free-vector/management-presents-work-plan-employee-optimization-meeting-room_1150-43192.jpg?w=996&t=st=1698414686~exp=1698415286~hmac=0b52a4815f12f67897d563109d9fbd8a3b88bfdf70e633cc60bc30e2050d9af5" alt="corporate">
      <h1 class="fw-bold">Innovative</h1>
      <h5>PissMC differs from other modloaders by targeting one of the most underrated versions of minecraft: rd-132211. While it was the first one to be released, at PissMC we believe that old doesn't equal to bad.</h5>
    </div>
    <div class="h-25 w-25 text-center">
      <img class="h-100 w-100" draggable="false" src="https://img.freepik.com/free-vector/couple-using-augmented-reality-smartphones_23-2148767243.jpg?w=996&t=st=1698414820~exp=1698415420~hmac=5fca5a5df626cfa12be150af20a7417b7cefd6464c0bbf0ab2f7662cfc238a5f" alt="corporate">
      <h1 class="fw-bold">Cool</h1>
      <h5>PissMC is just objectively cool. At school, they bully everybody who uses Forge and especially Fabric but if you mention that you use PissMC you will immediately get +50 points to your street cred.</h5>
    </div>
    <div class="h-25 w-25 text-center">
      <img class="h-100 w-100" draggable="false" src="https://img.freepik.com/free-vector/generation-x-abstract-concept-vector-illustration-middle-age-parents-work-life-balance-strong-professional-cold-war-personal-computing-pay-off-debt-stable-saving-plan-abstract-metaphor_335657-1920.jpg?w=996&t=st=1698414864~exp=1698415464~hmac=88e5ca0b68ccedef8366b123c442e06ae3d5434652f4ed511fa83d6c8994a888" alt="corporate">
      <h1 class="fw-bold">Lorem</h1>
      <h5>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sunt, praesentium vel. Vel, ipsum distinctio reiciendis expedita perspiciatis quod similique, sed ab, aliquam obcaecati laboriosam et. Sequi dolores quas harum fuga!</h5>
    </div>
  </div>

  <div class="bg-dark text-white text-center py-4">
    <p>ZeldaLord should activate windows</p>
    <p>God bootstrap is so bad</p>
    <div class="d-flex gap-3 justify-content-center">
      {#await get_installer_link()}
        <Button color="success">Get PissMC</Button>
      {:then link}
        <a href="{link}">
          <Button color="success">Get PissMC</Button>
        </a>
      {/await}
      <a href="https://modernmodpacks.site">
        <Button color="light">Checkout our actually good projects instead</Button>
      </a>
    </div>
  </div>
</main>
