import { describe, it, expect } from "vitest";

import { mount } from "@vue/test-utils";
import FlagMessage from "../FlagMessage.vue";

describe("FlagMessage", () => {
  it("renders properly", () => {
    const wrapper = mount(FlagMessage, {
      props: { content: "1st flag message" },
    });
    expect(wrapper.text()).toContain("1st flag message");
  });

  it("accepts modifiers", () => {
    const wrapper = mount(FlagMessage, {
      props: { content: "Flag message", modifier: "error" },
    });

    const flagMessage = wrapper.find(".flag-message");
    expect(flagMessage.element.className).toContain("error");
  });

  it("emits `close` when close button is clicked", async () => {
    const wrapper = mount(FlagMessage, {
      props: { content: "Flag message" },
    });

    const flagMessage = wrapper.find(".flag-message-close__icon");
    await flagMessage.trigger("click");
    expect(wrapper.emitted()).toHaveProperty("close");
  });
});
